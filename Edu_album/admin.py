from django.contrib import admin

# Register your models here.
from Edu_album.models import AlbumTeacher, AlbumAdult, AlbumTeenage, AlbumChildren, AlbumInstitute

admin.site.register(AlbumTeacher)
admin.site.register(AlbumAdult)
admin.site.register(AlbumTeenage)
admin.site.register(AlbumChildren)
admin.site.register(AlbumInstitute)
