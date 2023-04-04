from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return 'File id: ' + str(self.id)

