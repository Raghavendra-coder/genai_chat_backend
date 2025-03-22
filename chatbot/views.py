# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from aiintegration import ai_model, file_process_ai, summarize_text
# from .models import UploadedFile, TranscriptSegment
# from django.conf import settings
# from media_utility import extract_text_from_pdf, transcribe_audio, extract_audio_from_video
# import os
#
# ALLOWED_FILE_TYPES = ["pdf", "mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]
#
# class Index(APIView):
#     def get(self, request):
#         return Response({"message": "SUCCESS"})
#
# class ChatApi(APIView):
#     def post(self, request):
#         data = request.data
#         question = data.get("question", "")
#
#         if not question:
#             return Response({"error": "Question is required"}, status=400)
#
#         reply = ai_model(question)
#         return Response({"you": question, "Billa": reply})
#
# class FileSummarizeAPI(APIView):
#     def post(self, request):
#         file_obj = request.FILES.get("file", None)
#         question = request.data.get("question", "")
#
#         if not file_obj and not question:
#             return Response({"error": "Either a file or a question is required"}, status=400)
#
#         extracted_text = "Unsupported file type"
#         summarize = ""
#         file_answer = ""
#         transcript_segments = []
#         file_url = None
#
#         if file_obj:
#             file_extension = file_obj.name.split('.')[-1].lower()
#
#             if file_extension not in ALLOWED_FILE_TYPES:
#                 return Response(
#                     {"error": f"Unsupported file type: {file_extension}. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"},
#                     status=400)
#
#             file_instance = UploadedFile.objects.create(file=file_obj, file_type=file_extension)
#             file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
#
#             file_url = f"/media/{file_instance.file.name}"  # ✅ Fixed: Correct file URL
#
#             if file_extension == "pdf":
#                 extracted_text = extract_text_from_pdf(file_path)
#
#             elif file_extension in ["mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]:
#                 if file_extension in ["mp4", "mkv", "avi", "webm"]:
#                     audio_path = extract_audio_from_video(file_path)
#                 else:
#                     audio_path = file_path
#
#                 transcript_segments = transcribe_audio(audio_path)
#
#                 for segment in transcript_segments:
#                     TranscriptSegment.objects.create(
#                         file=file_instance,
#                         start_time=segment["start_time"],
#                         end_time=segment["end_time"],
#                         text=segment["text"]
#                     )
#
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             if extracted_text != "Unsupported file type":
#                 summarize = summarize_text(extracted_text)
#                 if question:
#                     file_answer = file_process_ai(extracted_text, question)
#
#             file_instance.extracted_text = extracted_text
#             file_instance.save()
#
#             response_data = {
#                 "file": file_obj.name if file_obj else None,
#                 "file_url": file_url,  # ✅ Return correct file URL
#                 "summarize": summarize,
#                 "answer": file_answer,
#                 "timestamps": transcript_segments
#             }
#
#         elif question:
#             question_answer = ai_model(question)
#             response_data = {"question": question, "answer": question_answer}
#         else:
#             response_data = {"error": "No question asked"}
#
#         return Response(response_data)
#
# class DeleteTranscriptionAPI(APIView):
#     def post(self, request):
#         UploadedFile.objects.all().delete()
#         TranscriptSegment.objects.all().delete()
#
#         media_root = os.path.join(settings.MEDIA_ROOT, "uploads")  # ✅ Fixed: Correct media folder path
#         if os.path.exists(media_root):
#             for filename in os.listdir(media_root):
#                 file_path = os.path.join(media_root, filename)
#                 try:
#                     os.remove(file_path)
#                 except Exception as e:
#                     print(f"Failed to delete {file_path}: {e}")
#
#         return Response({"message": "Previous transcription & media deleted!"})


# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from aiintegration import ai_model, file_process_ai, summarize_text
# from .models import UploadedFile, TranscriptSegment
# from django.conf import settings
# from media_utility import extract_text_from_pdf, transcribe_audio, extract_audio_from_video
# import os
#
# ALLOWED_FILE_TYPES = ["pdf", "mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]
# MIME_TYPE_MAP = {
#     "audio/mpeg": "mp3",
#     "audio/wav": "wav",
#     "audio/x-m4a": "m4a",
# }
#
# class Index(APIView):
#     def get(self, request):
#         return Response({"message": "SUCCESS"})
#
# class ChatApi(APIView):
#     def post(self, request):
#         data = request.data
#         question = data.get("question", "")
#
#         if not question:
#             return Response({"error": "Question is required"}, status=400)
#
#         reply = ai_model(question)
#         return Response({"you": question, "Billa": reply})
#
# class FileSummarizeAPI(APIView):
#     def post(self, request):
#         file_obj = request.FILES.get("file", None)
#         question = request.data.get("question", "")
#
#         if not file_obj and not question:
#             return Response({"error": "Either a file or a question is required"}, status=400)
#
#         extracted_text = "Unsupported file type"
#         summarize = ""
#         file_answer = ""
#         transcript_segments = []
#         file_url = None
#         is_video = False
#         is_audio = False
#
#         if file_obj:
#             file_extension = file_obj.name.split('.')[-1].lower()
#             content_type = file_obj.content_type
#
#             # ✅ Fix for MP3 issue
#             if content_type in MIME_TYPE_MAP:
#                 file_extension = MIME_TYPE_MAP[content_type]
#
#             if file_extension not in ALLOWED_FILE_TYPES:
#                 return Response({"error": f"Unsupported file type: {file_extension}. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"}, status=400)
#
#             file_instance = UploadedFile.objects.create(file=file_obj, file_type=file_extension)
#             file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
#             file_url = f"/media/{file_instance.file.name}"
#
#             if file_extension == "pdf":
#                 extracted_text = extract_text_from_pdf(file_path)
#
#             elif file_extension in ["mp3", "wav", "m4a"]:
#                 is_audio = True
#                 transcript_segments = transcribe_audio(file_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             elif file_extension in ["mp4", "mkv", "avi", "webm"]:
#                 is_video = True
#                 audio_path = extract_audio_from_video(file_path)
#                 transcript_segments = transcribe_audio(audio_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             if extracted_text != "Unsupported file type":
#                 summarize = summarize_text(extracted_text)
#                 if question:
#                     file_answer = file_process_ai(extracted_text, question)
#
#         return Response({
#             "file_url": file_url,
#             "is_video": is_video,
#             "is_audio": is_audio,
#             "summarize": summarize,
#             "answer": file_answer,
#             "timestamps": transcript_segments
#         })
#
# class DeleteTranscriptionAPI(APIView):
#     def post(self, request):
#         UploadedFile.objects.all().delete()
#         TranscriptSegment.objects.all().delete()
#
#         media_root = os.path.join(settings.MEDIA_ROOT, "uploads")
#         if os.path.exists(media_root):
#             for filename in os.listdir(media_root):
#                 file_path = os.path.join(media_root, filename)
#                 try:
#                     os.remove(file_path)
#                 except Exception as e:
#                     print(f"Failed to delete {file_path}: {e}")
#
#         return Response({"message": "Previous transcription & media deleted!"})


# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from aiintegration import ai_model, file_process_ai, summarize_text
# from .models import UploadedFile, TranscriptSegment
# from django.conf import settings
# from media_utility import extract_text_from_pdf, transcribe_audio, extract_audio_from_video
# import os
#
# ALLOWED_FILE_TYPES = ["pdf", "mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]
# MIME_TYPE_MAP = {
#     "audio/mpeg": "mp3",
#     "audio/wav": "wav",
#     "audio/x-m4a": "m4a",
# }
#
# class Index(APIView):
#     def get(self, request):
#         return Response({"message": "SUCCESS"})
#
# class ChatApi(APIView):
#     def post(self, request):
#         data = request.data
#         question = data.get("question", "")
#
#         if not question:
#             return Response({"error": "Question is required"}, status=400)
#
#         reply = ai_model(question)
#         return Response({"you": question, "Billa": reply})
#
# class FileSummarizeAPI(APIView):
#     def post(self, request):
#         file_obj = request.FILES.get("file", None)
#         question = request.data.get("question", "")
#
#         if not file_obj and not question:
#             return Response({"error": "Either a file or a question is required"}, status=400)
#
#         extracted_text = "Unsupported file type"
#         summarize = ""
#         file_answer = ""
#         transcript_segments = []
#         file_url = None
#         is_video = False
#         is_audio = False
#
#         if file_obj:
#             file_extension = file_obj.name.split('.')[-1].lower()
#             content_type = file_obj.content_type
#
#             if content_type in MIME_TYPE_MAP:
#                 file_extension = MIME_TYPE_MAP[content_type]
#
#             if file_extension not in ALLOWED_FILE_TYPES:
#                 return Response({"error": f"Unsupported file type: {file_extension}. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"}, status=400)
#
#             file_instance = UploadedFile.objects.create(file=file_obj, file_type=file_extension)
#             file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
#             file_url = f"/media/{file_instance.file.name}"
#
#             if file_extension == "pdf":
#                 extracted_text = extract_text_from_pdf(file_path)
#
#             elif file_extension in ["mp3", "wav", "m4a"]:
#                 is_audio = True
#                 transcript_segments = transcribe_audio(file_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             elif file_extension in ["mp4", "mkv", "avi", "webm"]:
#                 is_video = True
#                 audio_path = extract_audio_from_video(file_path)
#                 transcript_segments = transcribe_audio(audio_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             if extracted_text != "Unsupported file type":
#                 summarize = summarize_text(extracted_text)
#                 if question:
#                     file_answer = file_process_ai(extracted_text, question)
#
#         return Response({
#             "file_url": file_url,
#             "is_video": is_video,
#             "is_audio": is_audio,
#             "summarize": summarize,
#             "answer": file_answer,
#             "timestamps": transcript_segments
#         })
#
# class DeleteTranscriptionAPI(APIView):
#     def post(self, request):
#         UploadedFile.objects.all().delete()
#         TranscriptSegment.objects.all().delete()
#
#         media_root = os.path.join(settings.MEDIA_ROOT, "uploads")
#         if os.path.exists(media_root):
#             for filename in os.listdir(media_root):
#                 file_path = os.path.join(media_root, filename)
#                 try:
#                     os.remove(file_path)
#                 except Exception as e:
#                     print(f"Failed to delete {file_path}: {e}")
#
#         return Response({"message": "Previous transcription & media deleted!"})


# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from aiintegration import ai_model, file_process_ai, summarize_text
# from .models import UploadedFile, TranscriptSegment
# from django.conf import settings
# from media_utility import extract_text_from_pdf, transcribe_audio, extract_audio_from_video
# import os
#
# ALLOWED_FILE_TYPES = ["pdf", "mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]
# MIME_TYPE_MAP = {
#     "audio/mpeg": "mp3",
#     "audio/wav": "wav",
#     "audio/x-m4a": "m4a",
# }
#
#
# class Index(APIView):
#     def get(self, request):
#         return Response({"message": "SUCCESS"})
#
#
# class ChatApi(APIView):
#     def post(self, request):
#         data = request.data
#         question = data.get("question", "")
#
#         if not question:
#             return Response({"error": "Question is required"}, status=400)
#
#         reply = ai_model(question)
#         return Response({"you": question, "Billa": reply})
#
#
# class FileSummarizeAPI(APIView):
#     def post(self, request):
#         file_obj = request.FILES.get("file", None)
#         question = request.data.get("question", "")
#
#         if not file_obj and not question:
#             return Response({"error": "Either a file or a question is required"}, status=400)
#
#         extracted_text = "Unsupported file type"
#         summarize = ""
#         file_answer = ""
#         transcript_segments = []
#         file_url = None
#         is_video = False
#         is_audio = False
#
#         if file_obj:
#             file_extension = file_obj.name.split('.')[-1].lower()
#             content_type = file_obj.content_type
#
#             if content_type in MIME_TYPE_MAP:
#                 file_extension = MIME_TYPE_MAP[content_type]
#
#             if file_extension not in ALLOWED_FILE_TYPES:
#                 return Response(
#                     {"error": f"Unsupported file type: {file_extension}. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"},
#                     status=400)
#
#             file_instance = UploadedFile.objects.create(file=file_obj, file_type=file_extension)
#             file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
#             file_url = f"/media/{file_instance.file.name}"
#
#             if file_extension == "pdf":
#                 extracted_text = extract_text_from_pdf(file_path)
#
#             elif file_extension in ["mp3", "wav", "m4a"]:
#                 is_audio = True
#                 transcript_segments = transcribe_audio(file_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             elif file_extension in ["mp4", "mkv", "avi", "webm"]:
#                 is_video = True
#                 audio_path = extract_audio_from_video(file_path)
#                 transcript_segments = transcribe_audio(audio_path)
#                 extracted_text = " ".join([segment["text"] for segment in transcript_segments])
#
#             if extracted_text != "Unsupported file type":
#                 summarize = summarize_text(extracted_text)
#                 if question:
#                     file_answer = file_process_ai(extracted_text, question)
#
#         elif question:
#             file_answer = ai_model(question)
#
#         else:
#             file_answer = "no question or media"
#
#         return Response({
#             "file_url": file_url,
#             "is_video": is_video,
#             "is_audio": is_audio,
#             "summarize": summarize,
#             "answer": file_answer,
#             "timestamps": transcript_segments
#         })
#
#
# class DeleteTranscriptionAPI(APIView):
#     def post(self, request):
#         UploadedFile.objects.all().delete()
#         TranscriptSegment.objects.all().delete()
#
#         media_root = os.path.join(settings.MEDIA_ROOT, "uploads")
#         if os.path.exists(media_root):
#             for filename in os.listdir(media_root):
#                 file_path = os.path.join(media_root, filename)
#                 try:
#                     os.remove(file_path)
#                 except Exception as e:
#                     print(f"Failed to delete {file_path}: {e}")
#
#         return Response({"message": "Previous transcription & media deleted!"})


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from aiintegration import ai_model, file_process_ai, summarize_text
from .models import UploadedFile, TranscriptSegment
from django.conf import settings
from media_utility import extract_text_from_pdf, transcribe_audio, extract_audio_from_video
import os

ALLOWED_FILE_TYPES = ["pdf", "mp3", "wav", "m4a", "mp4", "mkv", "avi", "webm"]
MIME_TYPE_MAP = {
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "audio/x-m4a": "m4a",
}


class Index(APIView):
    def get(self, request):
        return Response({"message": "SUCCESS"})


class ChatApi(APIView):
    def post(self, request):
        data = request.data
        question = data.get("question", "")

        if not question:
            return Response({"error": "Question is required"}, status=400)

        reply = ai_model(question)
        return Response({"you": question, "Billa": reply})


class FileSummarizeAPI(APIView):
    def post(self, request):
        file_obj = request.FILES.get("file", None)
        question = request.data.get("question", "")

        if not file_obj and not question:
            return Response({"error": "Either a file or a question is required"}, status=400)

        extracted_text = "Unsupported file type"
        summarize = ""
        file_answer = ""
        transcript_segments = []
        file_url = None
        is_video = False
        is_audio = False

        if file_obj:
            file_extension = file_obj.name.split('.')[-1].lower()
            content_type = file_obj.content_type

            if content_type in MIME_TYPE_MAP:
                file_extension = MIME_TYPE_MAP[content_type]

            if file_extension not in ALLOWED_FILE_TYPES:
                return Response(
                    {"error": f"Unsupported file type: {file_extension}. Allowed: {', '.join(ALLOWED_FILE_TYPES)}"},
                    status=400)

            try:
                # Save uploaded file
                file_instance = UploadedFile.objects.create(file=file_obj, file_type=file_extension)
                file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)

                # Verify file exists
                if not os.path.exists(file_path):
                    return Response({"error": "File upload failed - please try again"}, status=500)

                file_url = f"/media/{file_instance.file.name}"

                if file_extension == "pdf":
                    extracted_text = extract_text_from_pdf(file_path)
                    file_instance.extracted_text = extracted_text
                    file_instance.save()

                elif file_extension in ["mp3", "wav", "m4a"]:
                    is_audio = True
                    transcript_segments = transcribe_audio(file_path)  # Pass original file path
                    extracted_text = " ".join([segment["text"] for segment in transcript_segments])

                elif file_extension in ["mp4", "mkv", "avi", "webm"]:
                    is_video = True
                    audio_path = extract_audio_from_video(file_path)
                    transcript_segments = transcribe_audio(audio_path)
                    extracted_text = " ".join([segment["text"] for segment in transcript_segments])
                    # Clean temporary audio
                    if os.path.exists(audio_path):
                        os.remove(audio_path)

                if extracted_text != "Unsupported file type":
                    summarize = summarize_text(extracted_text)
                    if question:
                        file_answer = file_process_ai(extracted_text, question)

            except Exception as e:
                return Response({"error": f"Processing failed: {str(e)}"}, status=500)

        elif question:
            file_answer = ai_model(question)

        return Response({
            "file_url": file_url,
            "is_video": is_video,
            "is_audio": is_audio,
            "summarize": summarize,
            "answer": file_answer,
            "timestamps": transcript_segments
        })


class DeleteTranscriptionAPI(APIView):
    def post(self, request):
        UploadedFile.objects.all().delete()
        TranscriptSegment.objects.all().delete()

        media_root = os.path.join(settings.MEDIA_ROOT, "uploads")
        if os.path.exists(media_root):
            for filename in os.listdir(media_root):
                file_path = os.path.join(media_root, filename)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

        return Response({"message": "Previous transcription & media deleted!"})
