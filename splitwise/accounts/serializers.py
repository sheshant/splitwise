from rest_framework import serializers

from django.contrib.auth.models import User

from accounts.models import UserTransaction


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


class UserTransactionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    own_to_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=False, allow_blank=True, max_length=100)
    price = serializers.FloatField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `UserTransaction` instance, given the validated data.
        """
        return UserTransaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `UserTransaction` instance, given the validated data.
        """
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.own_to_id = validated_data.get('own_to_id', instance.own_to_id)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
