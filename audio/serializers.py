from rest_framework import serializers
from .models import AudioBook, Song, Podcast


class AudioBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioBook
        fields = "__all__"
    
    def validate(self, data):
        if not isinstance(data.get("title"), str): raise serializers.ValidationError("Title must be string.")
        if not isinstance(data.get("author"), str): raise serializers.ValidationError("Author must be string.")
        if not isinstance(data.get("narrator"), str): raise serializers.ValidationError("Narrator must be string.")
        if data.get("title") == "" or data.get("author") == "" or data.get("narrator") == "" or data.get("title") == None or data.get("author") == None or data.get("narrator") == None:
            raise serializers.ValidationError("Title/Author/Narrator cannot be left empty.")
        elif len(data.get("title")) > 100 or len(data.get("author")) > 100 or len(data.get("narrator")) > 100: 
            raise serializers.ValidationError("Title/Author/Narrator cannot exceed 100 characters.")  
        if isinstance(data.get("duration"), int):
            if data.get("duration") <= 0:
                raise serializers.ValidationError("Duration must be a positive integer.") 
        else:
            raise serializers.ValidationError("Duration must be an positive integer.")
        return data

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
    
    def validate(self, data):
        if not isinstance(data.get("name"), str): raise serializers.ValidationError("Name must be string.")
        if not isinstance(data.get("host"), str): raise serializers.ValidationError("Host must be string.")
        if data.get("name") == "" or data.get("name") == None:
            raise serializers.ValidationError("Name cannot be left empty.")
        elif len(data.get("name")) > 100: 
            raise serializers.ValidationError("Name cannot exceed 100 characters.") 
        if data.get("host") == "" or data.get("host") == None:
            raise serializers.ValidationError("Host cannot be left empty.")
        elif len(data.get("host")) > 100: 
            raise serializers.ValidationError("Host cannot exceed 100 characters.") 
        if isinstance(data.get("duration"), int):
            if data.get("duration") <= 0:
                raise serializers.ValidationError("Duration must be a positive integer.") 
        else:
            raise serializers.ValidationError("Duration must be an positive integer.")
    
        return data

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"
    
    def validate(self, data):
        if not isinstance(data.get("name"), str): raise serializers.ValidationError("Name must be string.")
        if data.get("name") == "" or data.get("name") == None:
            raise serializers.ValidationError("Name cannot be left empty.")
        elif len(data.get("name")) > 100: 
            raise serializers.ValidationError("Name cannot exceed 100 characters.") 
        if isinstance(data.get("duration"), int):
            if data.get("duration") <= 0:
                raise serializers.ValidationError("Duration must be a positive integer.") 
        else:
            raise serializers.ValidationError("Duration must be an positive integer.")
        return data
