from typing import Optional, List
from datetime import datetime
from fastapi import FastAPI, Body, Query
from pydantic import BaseModel,Field, constr
from uuid import UUID

global Id 
# now = datetime.now()

class Song(BaseModel):
    Id: int 
    Name_of_the_song: str = Field(
        None, title="Name of the song ", max_length=100)
    Duration_number_of_seconds: int = Field(gt=0,
         title="Duration_number_of_seconds ")
    Uploaded_time : datetime


class Podcast(BaseModel):
    Id : int
    Name_of_the_podcast: str =Field(
        None, title="Name of the song ", max_length=100)
    Duration_in_number_of_seconds: int = Field(gt=0,
         title="Duration_number_of_seconds ")
    Uploaded_time :datetime
    Host : str =Field(
        None, title="Name of the song ", max_length=100)
    Participants : Optional[List[str]] = Field(None, max_length=100)
   

class Audiobook(BaseModel):
    Id : int
    Title_of_the_audiobook : str =Field(
        None, title="Name of the song ", max_length=100)
    Author_of_the_title : str =Field(
        None, title="Name of the song ", max_length=100)
    Narrator : str =Field(
        None, title="Name of the song ", max_length=100)
    Duration_in_number_of_seconds: int = Field(gt=0,
         title="Duration_number_of_seconds ") 
    Uploaded_time :datetime

app = FastAPI()


@app.post("/song/")
async def create_item(item: Song):
    item_dict = item.dict()
    # Id = UUID
    # item_dict.update({"Id": Id})
    return item_dict

@app.post("/podcast/")
async def create_item(item: Podcast):
    return item

@app.post("/audiobook/")
async def create_item(item: Audiobook):
    return item

@app.delete("/Song/{Song_Id}", response_model=Song, response_model_exclude_unset=True)
async def del_song()