from . import views
from django.urls import path
urlpatterns = [
    path("index/", views.Index.as_view(), name="index"),
    path("chat/", views.ChatApi.as_view(), name="chat"),
    path("file_summarize/", views.FileSummarizeAPI.as_view(), name="file_summarize"),
    path("delete_transcription/", views.DeleteTranscriptionAPI.as_view(), name="delete_transcription"),
]