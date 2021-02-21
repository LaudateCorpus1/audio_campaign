from flask import Flask, request
from datetime import datetime
from flasgger import Swagger
from pymongo import MongoClient

client = MongoClient()
db = client.Campaign
details = db.Campaign_details

app = Flask(__name__)
# swagger = Swagger(app)
# app.config.SWAGGER_VALIDATOR_URL = 'http://localhost:8080/validator'

Id_audio = 0
Id_song = 1
Id_podcast = 2

def Song(data):
    Id = Id_song + 1
    Name_of_the_song = data['Name_of_the_song']
    if type(Name_of_the_song) == str and Name_of_the_song and len(Name_of_the_song) < 100:
        name = Name_of_the_song
    else:
        name = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if type(Duration_number_of_seconds) == str and Duration_number_of_seconds and len(Duration_number_of_seconds) < 100:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded = datetime
    if Id and name and duration != None:
        return {
                "id":Id,
                "category": Song,
                "Name of the Song": name,
                "Duration_number_of_seconds": duration,
                "Uploaded_time": Uploaded
            }
    else:
        return 0

def audiobook(data):
    Id = Id_audio + 1
    Title_of_the_audiobook = data['Title of the audiobook']
    if type(Title_of_the_audiobook) == str and Title_of_the_audiobook and len(Title_of_the_audiobook) < 100:
        Title = Title_of_the_audiobook
    else:
        Title = None
    Author_of_the_title = data['Author of the title']
    if typr(Author_of_the_title) == str  and len(Author_of_the_title) < 100 and Author_of_the_title:
        author = Author_of_the_title
    else:
        author = None
    Narrator = data['Narrator']
    if typr(Narrator) == str  and len(Narrator) < 100 and Narrator:
        narrator = Narrator
    else:
        narrator = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if typr(Duration_number_of_seconds) == int  and len(Duration_number_of_seconds) > 0 and Duration_number_of_seconds:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded_time : datetime
    if Id and Title and narrator and duration != None:
        return {
                "Id": Id,
                "category": audiobook,
                "Title of the audiobook": Title,
                "Author of the title": author,
                "Narrator": narrator,
                "Duration_number_of_seconds": duration,
                "Upload Time": Uploaded_time
            }
    else:
        return 0



def podcast(data):
    Id = Id_podcast + 1
    Name_of_the_podcast = data['Name_of_the_podcast']
    if type(Name_of_the_podcast) == str and Name_of_the_podcast and len(Name_of_the_podcast) < 100:
        name = Name_of_the_podcast
    else:
        name = None
    Duration_number_of_seconds = data['Duration_number_of_seconds']
    if typr(Duration_number_of_seconds) == int  and len(Duration_number_of_seconds) > 0 and Duration_number_of_seconds:
        duration = Duration_number_of_seconds
    else:
        duration = None
    Uploaded_time : datetime
    Host = data['Host']
    if type(Host) == str and Host and len(Host) < 100:
        host = Name_of_the_podcast
    else:
        host = None

    participants = [data['Participants']]
    if len(participants) < 11:
        par = participants
    else:
        par = None
    if Id and name and duration and host != None:
        return {
                "Id": Id,
                "Name Of Podcast": name,
                "Duration": duration,
                "Uploaded Time": Uploaded_time,
                "Host": host,
                "participants": par
            }
    else:
        return 0







@app.route("/<audioFileType>", methods=['POST'])
def create_items(audioFileType):
    if audioFileType == "Song":
        data = request.get_json()
        print(data)
        a = Song(data)
        if a == 0:
            return {"message": "please check the details"}
        else:
            return {"message": "added to db succesfully"} 
    elif audioFileType == "Audiobook":
        data = request.get_json()
        b = audiobook(data)
        if b == 0:
            return {"message": "please check the details"}
        else:
            return {"message": "added to db succesfully"} 
    else:
        data = request.get_json()
        c = podcast(data)
        if c == 0:
            return {"message": "please check the details"}
        else:
            return {"message": "added to db succesfully"} 
    

@app.route("/<audioFileType>/<Id>", methods=['DELETE'])
def delete_items(audioFileType, Id):
    details.delete_one({"category":audioFileType, "Id":Id})
    return {"message": " deleted from db"}
        


@app.route("/<audioFileType>/<Id>", methods=['GET'])
def get_by_id(audioFileType, Id):
    a =details.find_one({"category":audioFileType, "Id": Id})
    return a


# @app.route("/<audioFileType>/<Id>", methods=['UPDATE']
# def update_audiofile(audioFileType, Id):

if __name__ == "__main__":
    app.run(port=8080)



