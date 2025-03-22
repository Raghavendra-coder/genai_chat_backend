from django.db import models

# Create your models here.
def upload_to(instance, filename):
    return f"uploads/{filename}"

class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_to)
    file_type = models.CharField(max_length=10)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class TranscriptSegment(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name="segments")
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()