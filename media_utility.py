import pdfplumber
from faster_whisper import WhisperModel
import ffmpeg
import os
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        return ""


def transcribe_audio(audio_path):
    """Handle both direct audio files and temporary video-extracted audio"""
    try:
        # Convert to MP3 if needed (for WAV/M4A)
        converted_path = audio_path
        original_format = audio_path.split('.')[-1].lower()

        if original_format not in ['mp3']:
            converted_path = f"{audio_path.rsplit('.', 1)[0]}.mp3"
            ffmpeg.input(audio_path).output(converted_path).run(overwrite_output=True)
            logger.info(f"Converted {original_format} to MP3: {converted_path}")

        model = WhisperModel("base")
        segments, _ = model.transcribe(converted_path)

        transcript = [
            {
                "start_time": float(segment.start),
                "end_time": float(segment.end),
                "text": segment.text
            }
            for segment in segments
        ]

        # Only delete converted files, keep original uploads
        if converted_path != audio_path and os.path.exists(converted_path):
            os.remove(converted_path)

        return transcript
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        return []


def extract_audio_from_video(video_path):
    try:
        audio_path = video_path.rsplit(".", 1)[0] + "_temp.mp3"
        ffmpeg.input(video_path).output(audio_path, format="mp3", acodec="libmp3lame").run(overwrite_output=True)
        return audio_path
    except Exception as e:
        logger.error(f"Audio extraction failed: {str(e)}")
        raise