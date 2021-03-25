from copy import error
import json
from json.decoder import JSONDecodeError

from rest_framework import serializers
from audio.serializers import AudioBookSerializer, PodcastSerializer, SongSerializer
from django.db.models.base import ModelBase
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .models import AudioBook, Song, Podcast
# Create your views here.

# stores the models to dynamically fetch based on the audio file type passed as a part of URL
audio_model = {
        "audiobook": AudioBook,
        "song": Song,
        "podcast": Podcast
    }
# Stores the serializers to dynamically call based on the audio file type passed as a part of URL
model_serializer = {
        "audiobook": AudioBookSerializer,
        "song": SongSerializer,
        "podcast": PodcastSerializer
    }

@method_decorator(csrf_exempt, name='dispatch')
class AudioView(View):
    # serialize the model data to JSON using ModelSerializers defined in serlizers.py
    def getJSON(self, querySet, audioFileType):
        serialized = None
        if isinstance(querySet, ModelBase):
            serialized = model_serializer[audioFileType](querySet.objects.all(), many=True)
        elif isinstance(querySet, (AudioBook, Song, Podcast,)):
            serialized = model_serializer[audioFileType](querySet)

        return serialized.data

    def get(self, request, **kwargs):
        # return a 400 status code if "audioFileType" is not found in the URL
        if not kwargs.get("audioFileType", None): return JsonResponse({ "error" : "Bad request" },status=400)
        audioFileType = kwargs.get("audioFileType", None)
        audioFileID = kwargs.get("audioFileID", None)
        audioObj = None

        # returns an 404 error if the audio file type passsed is invalid
        if audioFileType not in audio_model: return JsonResponse({ "error" : "'{}' is not a valid audio type".format(audioFileType) },status=404)

        if audioFileID is None:
            # fetchs the all the audio files of the provided audio type in JSON format
            audioObj = self.getJSON(audio_model[audioFileType], audioFileType)
        else:
            try:
                # fetchs the particular audio file of a audio type in JSON format
                # return 404 error if audio file of ID(audioFileID) does not exists. 
                audioObj = self.getJSON(audio_model[audioFileType].objects.get(id=audioFileID), audioFileType)
            except Exception as e:
                return JsonResponse({
                    "error": str(e)
                }, status=404)

        return JsonResponse({ audioFileType : audioObj}, status=200)

    def delete(self, request, **kwargs):
        # return a 400 status code if "audioFileType" is not found in the URL
        if not kwargs.get("audioFileType", None): return JsonResponse({ "error" : "Bad request" },status=400)
        audioFileType = kwargs.get("audioFileType", None)
        audioFileID = kwargs.get("audioFileID", None)

        # returns an 404 error if the audio file type passsed is invalid
        if audioFileType not in audio_model: return JsonResponse({ "error" : "'{}' is not a valid audio type".format(audioFileType) },status=404)

        if audioFileID is None:
            return JsonResponse({
                "message": "ID is required!"
            }, status=406)
        else:
            try:
                # fetchs the object of particular audio file of a audio type from the database
                audio = audio_model[audioFileType].objects.get(id=audioFileID)
                # fetchs its equivalent JSON format
                audioObj = self.getJSON(audio, audioFileType)
                audio.delete()
            except Exception as e:
                return JsonResponse({
                    "error": str(e)
                }, status=404)

        return JsonResponse({
            "message": "Deleted successfully",
            audioFileType: audioObj
        }, status=200)

    def post(self, request, **kwargs):
        # return a 400 status code if "audioFileType" is not found in the URL
        if kwargs.get("audioFileType", None): return JsonResponse({ "error" : "Bad request" },status=400)

        # Checks for any error while converting to JSON object from the request body,
        try:
            data =  json.loads(request.body)
        except JSONDecodeError as e:
            return JsonResponse({
                    "JSONDecodeError": str(e),
                    "message": "Please check if all the JSON keys-value pairs are of proper formatting."
                }, status=500)

        audioFileType = data.get("audioFileType", None)
                
        # returns an 404 error if the audio file type passsed is invalid
        if audioFileType not in audio_model: return JsonResponse({ "error" : "'{}' is not a valid audio type".format(audioFileType) },status=404)

        # Checks for Metadata in the request body, if not found raises en error
        audioFileMetadata = data.get("audioFileMetadata", None)
        if audioFileMetadata is None:
            return JsonResponse({ "message": "Metadata required!"}, status=406)

        # Since participants is an option parameter, the following code 
        # only check for number of participants and the character constraints
        participants = audioFileMetadata.get("participants")
        if participants: 
            if isinstance(participants, list):
                if len(participants) > 10:
                    return JsonResponse({ "message": "Participants can not be more than 10."}, status=406)
                for i in participants:
                    if not isinstance(i, str): return JsonResponse({ "message": "Participant must be a string."}, status=406)
                    elif len(i) > 100 : return JsonResponse({ "message": "Participant cannot exceed 100 characters."}, status=406)
            elif participants != None:
                return JsonResponse({ "message": "Participants must be an list of names."}, status=406)
        audioFileMetadata['participants'] = json.dumps(participants) if participants else None

        # create a new audio file record in the database
        serializer = model_serializer[audioFileType](data=audioFileMetadata)
        # if every thing is validated, saves the record entry and return the detail
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                audioFileType: serializer.data
            }, status=200)
        else:
            return JsonResponse({
                audioFileType: serializer.errors
            }, status=500)
        
    def put(self, request, **kwargs):
        # return a 400 status code if "audioFileType" is not found in the URL
        if not kwargs.get("audioFileType", None): return JsonResponse({ "error" : "Bad request" },status=400)

        # Checks for any error while converting to JSON object from the request body,
        try:
            data =  json.loads(request.body)
        except JSONDecodeError as e:
            return JsonResponse({
                    "JSONDecodeError": str(e),
                    "message": "Please check if all the JSON keys-value pairs are of proper formatting."
                }, status=500)

        audioFileType = kwargs.get("audioFileType", None)
        audioFileID = kwargs.get("audioFileID", None)

        # returns an 404 error if the audio file type passsed is invalid
        if audioFileType not in audio_model: return JsonResponse({ "error" : "'{}' is not a valid audio type".format(audioFileType) },status=404)

        # Checks for Metadata in the request body, if not found raises en error
        audioFileMetadata = data.get("audioFileMetadata", None)
        if audioFileMetadata is None:
            return JsonResponse({ "message": "Metadata required!"}, status=406)
        
        # Since participants is an option parameter, the following code 
        # only check for number of participants and the character constraints
        participants = audioFileMetadata.get("participants")
        if participants: 
            if isinstance(participants, list):
                if len(participants) > 10:
                    return JsonResponse({ "message": "Participants can not be more than 10."}, status=406)
                for i in participants:
                    if not isinstance(i, str): return JsonResponse({ "message": "Participant must be a string."}, status=406)
                    elif len(i) > 100 : return JsonResponse({ "message": "Participant cannot exceed 100 characters."}, status=406)
            elif participants != None:
                return JsonResponse({ "message": "Participants must be an list of names."}, status=406)
        
        audioFileMetadata['participants'] = json.dumps(participants) if participants else None

        if audioFileID is None:
            return JsonResponse({
                "message": "ID is required!"
            }, status=406)
        else:
            try:
                audio = audio_model[audioFileType].objects.get(id=audioFileID)
                audioObj = self.getJSON(audio, audioFileType)

                serializer = model_serializer[audioFileType](audio, data=audioFileMetadata, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return JsonResponse({
                        audioFileType: serializer.errors
                    }, status=500)
            except Exception as e:
                return JsonResponse({
                    "error": str(e)
                }, status=404)

        # returns the updated version of the record on successfull requuest completion
        return JsonResponse({
            audioFileType: serializer.data
        }, status=200)
    

def handler_500_server_error(request):
    return JsonResponse({
        "error": "Internal Server Error"
    }, status=500)