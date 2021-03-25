from django.urls import path, re_path
from .views import AudioView


urlpatterns = [
    path("", AudioView.as_view(), name="audioCreate"),
    path("<str:audioFileType>/<int:audioFileID>", AudioView.as_view(), name="audioFileFetch"),
    path("<str:audioFileType>/", AudioView.as_view(), name="audioFiles"),
]