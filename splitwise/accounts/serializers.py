from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer): # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.user.get_api_url(request=request)

    def validate_title(self, value):
        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username has already been taken")
        return value
