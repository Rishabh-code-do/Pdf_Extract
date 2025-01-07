from django.db import models

class Reasoning(models.Model):
    content = models.TextField()
    date = models.DateField()
    version_tag = models.CharField(max_length=50)
    security_tag = models.CharField(max_length=50)
    access_tag = models.CharField(max_length=20,default="all")

    def __str__(self):
        return f"Version {self.version_tag} ({self.date}) - {self.security_tag}"
