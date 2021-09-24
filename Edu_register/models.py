from django.db import models

# Create your models here.


class Register(models.Model):
    full_name = models.CharField(max_length=150)
    id_num = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    latest_course = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=300)
    birth = models.CharField(max_length=4)
    description = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name



from django.db import models
from django.core.files.storage import FileSystemStorage
import unicodedata

class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)
