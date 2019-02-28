from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.views import APIView

from accounts.models import UserProfile, UserActionLog
from accounts.serializers import UserSerializer
from accounts.utils import verify_transaction_data, add_transaction_data


class UserAPIView(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = UserSerializer
    UserActionLog_record = False

    def get_queryset(self):
        qs = User.objects.all()
        query = self.request.GET.get("query")
        if query is not None:
            qs = qs.filter(Q(username__icontains=query) |
                           Q(first_name__icontains=query) |
                           Q(last_name__icontains=query)).distinct()
            if not self.UserActionLog_record:
                UserActionLog.objects.get_or_create(user=self.request.user, action='search_user', action_data=query)
                self.UserActionLog_record = True
            else:
                self.UserActionLog_record = False

        return qs

    def perform_create(self, serializer):
        user = serializer.save()
        UserProfile.objects.create(user=user)
        UserActionLog.objects.create(user=self.request.user, action='created_user', action_data=user.username)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class UserAddTransactionView(APIView):
    def post(self, request):
        params = request.data
        result = verify_transaction_data(params)
        if result:
            return result
        return add_transaction_data(params)
