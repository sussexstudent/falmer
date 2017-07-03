from django.db import models


class FrontendDeployment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deployed_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
