from django.db import models
from django.contrib.auth import get_user_model # import user model

# Create your models here.
class Track(models.Model):
    # id field is auto added
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True) # optional
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True) # auto set to current DateTimeField
    posted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE) # posted by ?user using a many-to-one relationship and a CASCADE on_delete
