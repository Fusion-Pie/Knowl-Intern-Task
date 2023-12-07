from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Files(models.Model):
    file_name = models.CharField(max_length = 200)
    file = models.FileField()
    uploadedBy = models.ForeignKey(to = User, on_delete = models.CASCADE)
    shared_with = models.ManyToManyField(to = User, related_name = 'shared_with', blank = True)