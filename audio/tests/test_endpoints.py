from audio.models import AudioBook, Podcast, Song
import json
from django.test import TestCase
from django.urls import reverse
from pprint import pprint

class TestEndpoints(TestCase):
    def setUp(self):
        # setting up some test record entry in tables of database namely AudioBook, Podcast, Song
        # to test for the End Point
        AudioBook.objects.create(
            title="test_title",
            author="test_author",
            narrator="test_narrator",
            duration=223
        )
        Podcast.objects.create(
            name="test_podcast_name",
            host="test_host",
            duration=3423
        )
        Podcast.objects.create(
            name="test_podcast_name_2",
            host="test_host_2",
            duration=33
        )
        Song.objects.create(
            name="tset_song_name",
            duration=8457
        )
        Song.objects.create(
            name="test_song_name_2",
            duration=73868
        )
        return super().setUp()


    def test_audioCreate(self):
        """
            Used to test Create API
        """
        url = reverse("audioCreate")
        print ("\n########## Create API ##########")
        # GET method for audio file creation
        get_resp = self.client.get(url)
        print ("status_code : {}, get content : ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEqual(get_resp.status_code, 400 or 404 or 406)

        # POST method for audio file creation without any metadata
        post_resp = self.client.post(url)
        print ("status_code : {}, post content : ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertEqual(post_resp.status_code, 500)

        # POST method for audio file creation with incomplete metadata
        post_data = {
            "audioFileType": "song", 
            "audioFileMetadata" : {
                "name": "",
                "duration": 90
            }
        }
        post_resp = self.client.post(url, data=post_data, content_type="application/json")
        print ("status_code : {}, post content : ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertEqual(post_resp.status_code, 500)

        # POST method for audio file creation with improper metadata
        post_data = {
            "audioFileType": "audiobook", 
            "audioFileMetadata" : {
                "title": "test_case_title",
                "duration": 90,
                "author": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum",
                "narrator": "test_narrator_name" 
            }
        }
        post_resp = self.client.post(url, data=post_data, content_type="application/json")
        print ("status_code : {}, post method(audiobook) : ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertEqual(post_resp.status_code, 500)


        # POST method for audio file creation with proper metadata
        post_data = {
            "audioFileType": "song", 
            "audioFileMetadata" : {
                "name": "test_case_name",
                "duration": 90
            }
        }
        post_resp = self.client.post(url, data=post_data, content_type="application/json")
        print ("status_code : {}, post method(song) : ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertEqual(post_resp.status_code, 200)

        # POST method for audio file creation with complete and proper metadata
        post_data = {
            "audioFileType": "audiobook", 
            "audioFileMetadata" : {
                "title": "test_case_title_1",
                "duration": 90,
                "author": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
                "narrator": "test_narrator_name_1" 
            }
        }
        post_resp = self.client.post(url, data=post_data, content_type="application/json")
        print ("status_code : {}, post method(audiobook) : ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertEqual(post_resp.status_code, 200)

    def test_audioFiles(self):
        """
            Used to test GET API for all audio file of a audio file type.
        """
        print ("\n\n########## GET API ##########")
        audiobook_url = reverse("audioFiles", args=["audiobook"])
        song_url = reverse("audioFiles", args=["song"])
        podcast_url = reverse("audioFiles", args=["podcast"])

        # Tests for GET Method to fetch all the audiobooks files
        # while fetching audio files it is also checking for the returned data's datatype
        get_resp = self.client.get(audiobook_url)
        print ("status_code : {}, get method(audiobook): ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEquals(get_resp.status_code, 200)
        self.assertIsInstance(json.loads(get_resp.content), dict)
        self.assertIsInstance(json.loads(get_resp.content)["audiobook"], list)
        self.assertNotIsInstance(json.loads(get_resp.content)["audiobook"], (str,int,dict,set))

        # Tests for GET Method to fetch all the songs files
        # while fetching audio files it is also checking for the returned data's datatype
        get_resp = self.client.get(song_url)
        print ("status_code : {}, get method(song): ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEquals(get_resp.status_code, 200)
        self.assertIsInstance(json.loads(get_resp.content), dict)
        self.assertIsInstance(json.loads(get_resp.content)["song"], list)
        self.assertNotIsInstance(json.loads(get_resp.content)["song"], (str,int,dict,set))

        # Tests for GET Method to fetch all the podcasts files
        # while fetching audio files it is also checking for the returned data's datatype
        get_resp = self.client.get(podcast_url)
        print ("status_code : {}, get method(podcast): ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEquals(get_resp.status_code, 200)
        self.assertIsInstance(json.loads(get_resp.content), dict)
        self.assertIsInstance(json.loads(get_resp.content)["podcast"], list)
        self.assertNotIsInstance(json.loads(get_resp.content)["podcast"], (str,int,dict,set))

        # Tests for POST Method at wrong EndPoint
        post_resp = self.client.post(audiobook_url)
        print ("status_code : {}, post method(podcast): ".format(post_resp.status_code), end="\n")
        pprint(json.loads(post_resp.content))
        self.assertNotEquals(post_resp.status_code, 200)

        # Tests for PUT Method without metadata
        put_resp = self.client.put(song_url)
        print ("status_code : {}, put method(podcast): ".format(put_resp.status_code), end="\n")
        pprint(json.loads(put_resp.content))
        self.assertNotEquals(put_resp.status_code, 200)

        # Tests for DELETE Method without an audio file ID
        del_resp = self.client.delete(podcast_url)
        print ("status_code : {}, del method(podcast): ".format(del_resp.status_code), end="\n")
        pprint(json.loads(del_resp.content))
        self.assertNotEquals(del_resp.status_code, 200)

    def test_audioFileFetch(self):
        """
            Used to test GET/PUT/DELETE API for particular audio file.
        """
        print ("\n\n########## GET/PUT/DELETE API ##########")
        audiobook_url = reverse("audioFileFetch", args=["audiobook", "10"])
        song_url = reverse("audioFileFetch", args=["song", "1"])
        podcast_url = reverse("audioFileFetch", args=["podcast", "2"])

        # Tests for GET Method to fetch a particular audiobook
        get_resp = self.client.get(audiobook_url)
        print ("status_code : {}, get method(audiobook): ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEquals(get_resp.status_code, 404)
        self.assertEquals(json.loads(get_resp.content)["error"], "AudioBook matching query does not exist.")

        # Tests for GET Method to fetch a particular song
        get_resp = self.client.get(song_url)
        print ("status_code : {}, get method(song): ".format(get_resp.status_code), end="\n")
        pprint(json.loads(get_resp.content))
        self.assertEquals(get_resp.status_code, 200)

        # Tests for PUT Method to update an audio file
        # here audio file type (Song) with ID(1) is being updated
        put_data = {
            "audioFileMetadata": {
                "name": "Himanshu Shende",
                "duration": 6759
            }
        }
        put_resp = self.client.put(song_url, data=put_data, content_type='application/json')
        print ("status_code : {}, put method(song): ".format(put_resp.status_code), end="\n")
        pprint(json.loads(put_resp.content))
        self.assertEquals(put_resp.status_code, 200)

        # Tests for DELETE Method 
        # here audio file type (Podcast) with ID(2) is being deleted
        del_resp = self.client.delete(podcast_url)
        print ("status_code : {}, del method(podcast): ".format(del_resp.status_code), end="\n")
        pprint(json.loads(del_resp.content))
        self.assertEquals(del_resp.status_code, 200)
