from bson import json_util
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flasgger import Swagger
from pymongo import MongoClient

client = MongoClient()
db = client.audio
details = db.Campaign_details

app = Flask(__name__)
# swagger = Swagger(app)
# app.config.SWAGGER_VALIDATOR_URL = 'http://localhost:8080/validator'

Id_audio = 21
Id_song = 1
Id_podcast = 71


def update_id():
    global Id_song
    global Id_audio
    global Id_podcast
    Id_song += 1
    Id_audio += 1
    Id_podcast += 1


def Song(data, Id):
    # Id = Id + 1
    Name_of_song = data['Name_of_the_Song']
    if type(Name_of_song) == str and len(Name_of_song) < 100:
        name = Name_of_song
    else:
        name = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if type(Duration_number_of_seconds) == int and Duration_number_of_seconds > 100:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded = datetime.now()
    if (name and duration) is not None:
        data_song = {
            "Id": Id,
            "category": "song",
            "Name_of_the_Song": name,
            "Duration_number_of_seconds": duration,
            "Uploaded_time": Uploaded
        }
        update_id()
        return data_song
    else:
        return 0


def audiobook(data, Id):
    # Id = Id_audio + 1
    Title_of_the_audiobook = data['Title_of_the_audiobook']
    if type(Title_of_the_audiobook) == str and len(Title_of_the_audiobook) < 100:
        Title = Title_of_the_audiobook
    else:
        Title = None
    Author_of_the_title = data['Author_of_the_title']
    if type(Author_of_the_title) == str and len(Author_of_the_title) < 100:
        author = Author_of_the_title
    else:
        author = None
    Narrator = data['Narrator']
    if type(Narrator) == str and len(Narrator) < 100:
        narrator = Narrator
    else:
        narrator = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if type(Duration_number_of_seconds) == int and Duration_number_of_seconds > 0:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded_time = datetime.now()
    if (Id and Title and narrator and duration) is not None:
        data_audio = {
            "Id": Id,
            "category": "audiobook",
            "Title_of_the_audiobook": Title,
            "Author_of_the_title": author,
            "Narrator": narrator,
            "Duration_number_of_seconds": duration,
            "Upload_time": Uploaded_time
        }
        update_id()
        return data_audio
    else:
        return 0


def podcast(data, Id):
    Name_of_the_podcast = data['Name_of_the_podcast']
    if type(Name_of_the_podcast) == str and Name_of_the_podcast and len(Name_of_the_podcast) < 100:
        name = Name_of_the_podcast
    else:
        name = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if type(Duration_number_of_seconds) == int and Duration_number_of_seconds > 0:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded_time = datetime.now()
    Host = data['Host']
    if type(Host) == str and Host and len(Host) < 100:
        host = Name_of_the_podcast
    else:
        host = None

    participants = data['Participants']
    if len(participants) < 11:
        par = participants
    else:
        par = None
    if (Id and name and duration and host) is not None:
        data_podcast = {
            "Id": Id,
            "category": "podcast",
            "Name_of_the_podcast": name,
            "Duration_number_of_seconds": duration,
            "Uploaded_time": Uploaded_time,
            "Host": host,
            "participants": par
        }
        update_id()
        return data_podcast


@app.route("/<audioFileType>", methods=['POST'])
def create_items(audioFileType):
    if audioFileType == "song":
        data = request.get_json()
        songdata = Song(data, Id_song)
        print(songdata)
        if details.insert_one(songdata):
            return jsonify({"Response": "added to db"})
        else:
            return jsonify({"error": "error"})
    elif audioFileType == "audiobook":
        data2 = request.get_json()
        audiodata = audiobook(data2, Id_audio)
        if details.insert_one(audiodata):
            return jsonify({"Response": "added to db"})
        else:
            return jsonify({"error": "error"})
    elif audioFileType == "podcast":
        data3 = request.get_json()
        podcastdata = podcast(data3, Id_podcast)
        if details.insert_one(podcastdata):
            return jsonify({"Response": "added to db"})
        else:
            return jsonify({"error": "error"})
    else:
        return {"error": "invalid url"}


@app.route("/<audioFileType>/<int:Id>", methods=['DELETE'])
def delete_items(audioFileType, Id):
    if details.delete_one({"category": audioFileType, "Id": Id}):
        return {"message": " deleted from db"}
    else:
        return 0


def get_data(category, Id):
    data = details.find_one({'category': category, 'Id': Id})
    print(data)
    return json_util.dumps(data)


@app.route("/<audioFileType>/<int:Id>", methods=['GET'])
def get_by_id(audioFileType, Id):
    print(audioFileType, Id)
    d = get_data(audioFileType, Id)
    return d


@app.route("/<audioFileType>/<int:Id>", methods=['PUT'])
def update_audiofile(audioFileType, Id):
    filter = {"category": audioFileType, "Id": Id}
    if audioFileType == "song":
        data = request.get_json()
        newvalues = {"$set": {'Name_of_the_Song': data['Name_of_the_Song'],
                              'Duration_number_of_seconds': data['Duration_number_of_seconds']
                              }
                     }
        if details.update_one(filter, newvalues):
            return {"message": "updated Song to Db"}
    elif audioFileType == "audiobook":
        data2 = request.get_json()
        update_audiobook = {"$set": {"Title_of_the_audiobook": data2['Title_of_the_audiobook'],
                                     "Author_of_the_title": data2['Author_of_the_title'],
                                     "Narrator": data2['Narrator'],
                                     "Duration_number_of_seconds": data2['Duration_number_of_seconds'],
                                     "Upload_time": datetime.now()
                                     }
                            }
        if details.update_one(filter, update_audiobook):
            return {"message": "updated audiobook to Db"}
    else:
        data3 = request.get_json()
        update_podcast = {"$set": {"Name_of_the_podcast": data3['Name_of_the_podcast'],
                                   "Duration_number_of_seconds": data3['Duration_number_of_seconds'],
                                   "Host": data3['Host'],
                                   "Uploaded_time": datetime.now(),
                                   "participants": data3['participants']
                                   }
                          }
        if details.update_one(filter, update_podcast):
            return {"message": "podcast updated to Db"}


if __name__ == "__main__":
    app.run('127.0.0.1', port=5555)
