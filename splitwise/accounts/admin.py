from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import UserProfile, UserActionLog


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'image_tag', 'date_joined')
    search_fields = ('username', 'email', 'date_joined')

    def image_tag(self, obj):
        return '<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.user.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'is_active', 'user_link', 'image_tag', )
    readonly_fields = ('image_tag',)

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def email(obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

    def user_link(self, obj):
        user = obj.user
        return '<a href="{}" target="_blank">{}</a>'.format(reverse("admin:auth_user_change", args=(user.id,)),
                                                            escape(user.username))

    user_link.allow_tags = True

    def image_tag(self, obj):
        return u'<img src="/static/%s" style="max-height:40px;max-width:40px">' % obj.photo_path.url.split('/')[-1]

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'action_time', 'action_data')
    search_fields = ('action', 'action_time', )
    date_hierarchy = 'action_time'
    list_filter = (
        ('action_time', DateFieldListFilter),
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserActionLog, UserActionLogAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

