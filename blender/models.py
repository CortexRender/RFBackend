from django.db import models

class Document(models.Model):
    # Name, user info, or any other metadata fields
    upload = models.FileField()
    # Or: upload = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.upload.name
