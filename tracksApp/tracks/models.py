from django.db import models

# Create your models here.
class Track(models.Model):
    # id field is auto added
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True) # optional
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True) # auto set to current DateTimeField
