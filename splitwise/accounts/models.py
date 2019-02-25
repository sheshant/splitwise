import os

from django.db import models
from django.contrib.auth.models import User
from rest_framework.reverse import reverse as api_reverse
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo_path = models.ImageField(upload_to='images/', default=os.path.join(settings.BASE_DIR, 'images/xrSh9Z0.jpg'))

    def __str__(self):
        return str(self.user.username)

    def get_api_url(self, request=None):
        return api_reverse("accounts:post-rud", kwargs={'pk': self.user.pk}, request=request)


class UserActionLog(models.Model):
    user = models.ForeignKey(User, related_name='user_action_log', on_delete=models.CASCADE)
    action = models.CharField(default='', max_length=256)
    action_data = models.CharField(default='', max_length=256)
    action_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
