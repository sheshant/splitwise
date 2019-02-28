import os
from datetime import datetime

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


class UserGroup(models.Model):
    group_name = models.CharField(default='', max_length=256)
    users = models.ManyToManyField(User, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    las_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class UserTransaction(models.Model):
    user = models.ForeignKey(User, related_name='user_transactions', on_delete=models.CASCADE)
    own_to = models.ForeignKey(User, related_name='user_transactions_owned', on_delete=models.CASCADE)
    reason = models.CharField(default='', max_length=256)
    price = models.FloatField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    las_modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'user {} own {} rupees to {} on {} for {}'.format(self.user.username, self.price, self.own_to,
                                                                 self.created_at, self.reason)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.las_modified_at = datetime.now()
        return super(UserTransaction, self).save(*args, **kwargs)

