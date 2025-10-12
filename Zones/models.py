from django.db import models
from django.utils import timezone


# Create your models here.
class Zone(models.Model):
    ZONE_TYPES = [
        ('extremely_dangerous', 'Extremely Dangerous'),
        ('dangerous', 'Dangerous'),
        ('relatively_unsafe', 'Relatively Unsafe'),
        ('accident_zone', 'Accident Zone'),
        ('wildlife_danger', 'Wildlife Danger'),
    ]
    type = models.CharField(
        max_length=50,
        choices=ZONE_TYPES,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(default=100.0, help_text="Radius in meters")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
