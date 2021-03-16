from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, DateTimeField, IntField, FloatField, ListField, DictField, connect, disconnect_all
import datetime
from dateutil import parser

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'AudioDB',
    'host':'localhost',
    'port': 27017
}
db = MongoEngine(app)

class Song(Document):
    """
        ID – (mandatory, integer, unique)
        Name of the song – (mandatory, string, cannot be larger than 100 characters)
        Duration in number of seconds – (mandatory, integer, positive)
        Uploaded time – (mandatory, Datetime, cannot be in the past)
    """
    Uploadedtime = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ID = IntField(unique=True, required=True)
    NameofSong = StringField(max_length=100, required=True)
    Duration = IntField(required=True, min_value=0)


class Podcast(Document):
    """
        ID – (mandatory, integer, unique)
        Name of the podcast – (mandatory, string, cannot be larger than 100 characters)
        Duration in number of seconds – (mandatory, integer, positive)
        Uploaded time – (mandatory, Datetime, cannot be in the past)
        Host – (mandatory, string, cannot be larger than 100 characters)
        Participants – (optional, list of strings, each string cannot be larger than 100 characters,
                        maximum of 10 participants possible)
    """
    Uploadedtime = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ID = IntField(unique=True, required=True)
    NameofPodcast = StringField(max_length=100, required=True)
    Duration = IntField(required=True, min_value=0)
    Host = StringField(max_length=100)
    Participants = ListField(optional=True)


class AudioBook(Document):
    """
        ID – (mandatory, integer, unique)
        Title of the audiobook – (mandatory, string, cannot be larger than 100 characters)
        Author of the title (mandatory, string, cannot be larger than 100
        characters)
        Narrator - (mandatory, string, cannot be larger than 100 characters)
        Duration in number of seconds – (mandatory, integer, positive)
        Uploaded time – (mandatory, Datetime, cannot be in the past)
    """
    Uploadedtime = DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ID = IntField(unique=True, required=True)
    Title = StringField(max_length=100, required=True)
    Duration = IntField(required=True, min_value=0)
    Author = StringField(max_length=100)
    Narrator = StringField(max_length=100)


@app.route('/create', methods=['POST'])
def create():
    reqdata = request.get_json()
    audioFileType = reqdata['audioFileType']
    audioFileMetadata = reqdata['audioFileMetadata']
    # print(audioFileMetadata['ID'])
    if audioFileType == 'song':
        song = Song(ID=audioFileMetadata['ID'],
                        NameofSong=audioFileMetadata['Name'],
                        Duration=audioFileMetadata['Duration'],
                        Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']))
        # print(song)
        song.save()
        return {"success": True}, 200
        
    if audioFileType == 'podcast':
        podcast = Podcast(ID=audioFileMetadata['ID'], 
                            NameofPodcast=audioFileMetadata['Name'],
                            Duration=audioFileMetadata['Duration'], 
                            Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']),
                            Host=audioFileMetadata['Host'], 
                            Participants=audioFileMetadata['Participants'] if len(audioFileMetadata['Participants'])>1 else None)
        podcast.save()

    if audioFileType == 'audiobook':
        audiobook = AudioBook(ID=audioFileMetadata['ID'], 
                                Title=audioFileMetadata['Name'],
                                Duration=audioFileMetadata['Duration'], 
                                Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']),
                                Author=audioFileMetadata['Author'], 
                                Narrator=audioFileMetadata['Narrator'])
        audiobook.save()
    return {"success": True}, 200


@app.route('/<audioFileType>', methods=['GET'])
def getall(audioFileType):
    """
        The route “<audioFileType>/<audioFileID>” will return the specific audio file
        The route “<audioFileType>” will return all the audio files of that type
    """

    if audioFileType == 'song':
        data = Song.objects()
        return jsonify(data), 200
        
    elif audioFileType == 'podcast':
        data = Podcast.objects()
        return jsonify(data), 200

    elif audioFileType == 'audiobook':
        data = AudioBook.objects()
        return jsonify(data), 200
    
    else:
        return "Please Check the Audio File Type", 200


@app.route('/<audioFileType>/<audioFileID>', methods=['GET'])
def getbyid(audioFileType, audioFileID):
    """
        The route “<audioFileType>/<audioFileID>” will return the specific audio file
        The route “<audioFileType>” will return all the audio files of that type
    """

    if audioFileType == 'song':
        data = Song.objects(ID=audioFileID)
        return jsonify(data), 200
        
    elif audioFileType == 'podcast':
        data = Podcast.objects(ID=audioFileID)
        return jsonify(data), 200

    elif audioFileType == 'audiobook':
        data = AudioBook.objects(ID=audioFileID)
        return jsonify(data), 200
    
    else:
        return "Please Check the Audio File Type or the ID", 200


@app.route('/<audioFileType>/<audioFileID>', methods=['PUT'])
def updatebyid(audioFileType, audioFileID):
    """
        The route be in the following format: “<audioFileType>/<audioFileID>”
        The request body will be the same as the upload
    """

    if audioFileType == 'song':
        audioFileMetadata = request.get_json()['audioFileMetadata']
        data = Song.objects(ID=audioFileID)
        data.update(ID=audioFileMetadata['ID'],
                        NameofSong=audioFileMetadata['Name'],
                        Duration=audioFileMetadata['Duration'],
                        Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']))
        return jsonify(data), 200
        
    elif audioFileType == 'podcast':
        audioFileMetadata = request.get_json()['audioFileMetadata']
        data = Podcast.objects(ID=audioFileID)
        data.update(ID=audioFileMetadata['ID'], 
                            NameofPodcast=audioFileMetadata['Name'],
                            Duration=audioFileMetadata['Duration'], 
                            Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']),
                            Host=audioFileMetadata['Host'], 
                            Participants=audioFileMetadata['Participants'] if len(audioFileMetadata['Participants'])>1 else None)
        return jsonify(data), 200

    elif audioFileType == 'audiobook':
        audioFileMetadata = request.get_json()['audioFileMetadata']
        data = AudioBook.objects(ID=audioFileID)
        data.update(ID=audioFileMetadata['ID'], 
                                Title=audioFileMetadata['Name'],
                                Duration=audioFileMetadata['Duration'], 
                                Uploadedtime= parser.parse(audioFileMetadata['Uploadedtime']),
                                Author=audioFileMetadata['Author'], 
                                Narrator=audioFileMetadata['Narrator'])
        return jsonify(data), 200
    
    else:
        return "Please Check the Audio File Type or the ID", 200


@app.route('/<audioFileType>/<audioFileID>', methods=['DELETE'])
def deletebyid(audioFileType, audioFileID):
    """
        The route “<audioFileType>/<audioFileID>” will return the specific audio file
        The route “<audioFileType>” will return all the audio files of that type
    """

    if audioFileType == 'song':
        data = Song.objects(ID=audioFileID)
        deleted = data.delete()
        if deleted:
            return "Deleted", 200 

        
    elif audioFileType == 'podcast':
        data = Podcast.objects(ID=audioFileID)
        deleted = data.delete()
        if deleted:
            return "Deleted", 200 

    elif audioFileType == 'audiobook':
        data = AudioBook.objects(ID=audioFileID)
        deleted = data.delete()
        if deleted:
            return "Deleted", 200
    
    else:
        return "Please Check the Audio File Type or the ID", 200


if __name__ == "__main__":
    app.run()