from django.db import models

# Create your models here.
from Edu_course.models import upload_image_path


class Level(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    short_description = models.TextField()

    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def get_absolute_url(self):
        return f"/levels-detail/{self.id}"




