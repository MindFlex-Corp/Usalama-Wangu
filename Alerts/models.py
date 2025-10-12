from django.db import models


# Create your models here.
class Alert(models.Model):
    alert_type = models.CharField(max_length=100, default="emergency_panic_button")
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=255, blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    audio_url = models.URLField()
    notified_contacts = models.JSONField(default=list, blank=True)
    delivered_to_authorities = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alert ({self.alert_type}) by {'Anonymous'} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class SMS(models.Model):
    alert = models.ForeignKey(Alert,on_delete=models.CASCADE,related_name="sms_messages")
    to = models.CharField(max_length=20)
    from_number = models.CharField(max_length=20)
    message_body = models.TextField()

    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("pending", "Pending"),
    ]
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SMS to {self.to} ({self.status})"
