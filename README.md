# Filed.com Coding Task

Install requirement.txt :  
*`python -m pip install -r requirements.txt`*

To run test enter following code :\
*`python manage.py test audio`*

# Endpoints:
## Create API <br>
**POST**  http://localhost:8000/ <br>
**body payload(JSON)** : `
{
    "audioFileType" : "audiobook",
    "audioFileMetadata": {
        "title": "test_audiobook",
        "duration": 59,
        "narrator": "test_narrator",
        "author": "test_author"
    }
}
`


## GET API <br>
**GET**  http://localhost:8000/podcast/ <br>
to get all the podcast files <br>
 **GET**  http://localhost:8000/song/ <br>
to get all the song files <br>
**GET**  http://localhost:8000/audiobook/ <br>
to get all the audiobook files <br>
**GET**  http://localhost:8000/podcast/1/ <br>
to get a particular podcast file <br>
 **GET**  http://localhost:8000/song/2/ <br>
to get a particular song file <br>
**GET**  http://localhost:8000/audiobook/3/ <br>
to get a particular audiobook file <br>


## Update API <br>
**PUT**  http://localhost:8000/audiobook/1/ <br>
**body payload(JSON)** : `
{
    "audioFileMetadata": {
        "title": "new_title",
        "duration": 519,
        "narrator": "changed",
        "author": "test_author"
    }
}` 
<br>
**PUT**  http://localhost:8000/podcast/1/ <br>
**body payload(JSON)** : `
{
    "audioFileMetadata": {
        "name": "new_name",
        "duration": 259,
        "host": "same",
        "participants": ["p1", "p2", "p3"],
    }
}
`
<br>
**PUT**  http://localhost:8000/song/2/ <br>
**body payload(JSON)** : `
{
    "audioFileMetadata": {
        "name": "new_name",
        "duration": 596
    }
}

**Output Example**: `{
    "audiobook": {
        "id": 3,
        "title": "test_title",
        "author": "author_test",
        "narrator": "narrator_test_1",
        "duration": 409,
        "uploaded_time": "2021-03-25T22:04:54.879689Z"
    }
}`

**Note**: only required and mentioned metadata are accepted based on the audio file type, others are ignored even if passed as a part of metadata <br>

## DELETE API <br>
**DELETE**  http://localhost:8000/audiobook/1/ <br>
**DELETE**  http://localhost:8000/song/1/ <br>
**DELETE**  http://localhost:8000/podcast/1/ <br>

**OutPut Example**:`{
    "message": "Deleted successfully",
    "song": {
        "id": 4,
        "name": "something",
        "duration": 324,
        "uploaded_time": "2021-03-25T13:20:41.442365Z"
    }
}`
