


from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .models import UserProfile
from . import serializers

User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    Endpoint for user registration.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserRegistrationSerializer
    queryset = User.objects.all()


class UserEmailVerificationAPIView(views.APIView):
    """
    Endpoint for verifying email address.

    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, verification_key):
        activated_user = self.activate(verification_key)
        if activated_user:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def activate(self, verification_key):
        return UserProfile.objects.activate_user(verification_key)


class UserLoginAPIView(views.APIView):
    """
    Endpoint for user login. Returns authentication token on success.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(views.APIView):
    """
    Endpoint to send email to user with password reset link.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request):
        user_profile = self.get_user_profile(request.data.get('email'))
        if user_profile:
            user_profile.send_password_reset_email(
                site=get_current_site(request)
            )  # To be made asynchronous in production
            return Response(status=status.HTTP_200_OK)

        # Forcing Http status to 200 even if failure to support user privacy.
        # Will show message at frontend like "If the email is valid, you must have received password reset email"
        return Response(status=status.HTTP_200_OK)

    def get_user_profile(self, email):
        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except:
            return None
        return user_profile


class PasswordResetConfirmView(views.APIView):
    """
    Endpoint to change user password.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={
                'uidb64': kwargs['uidb64'],
                'token': kwargs['token']
            })

        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data.get('new_password')
            user = serializer.user
            user.set_password(new_password)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Endpoint to retrieve user profile.

    """

    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile



# from django.shortcuts import render
# from rest_framework import serializers
# from rest_framework import generics, mixins,status, viewsets
# from .models import *
# from .serializers import *
# from rest_framework.response import Response
#
#
# # Create your views here.
#
# class ClassListView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin):
#     serializer_class = ClassSerializer
#     queryset = ClassesModel.objects.filter()
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self,request):
#         return self.create(request)
#
#
# # class AdminListView(generics.GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin):
# #     serializer_class = AdminSerializer
# #     queryset = AdminModel12.objects.all()
# #
# #     def get(self, request):
# #         return self.list(request)
# #
# #     def post(self,request):
# #         return self.create(request)
#
#
# class DivListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
#     serializer_class = DivSerializer
#     queryset = DivModel.objects.all()
#     lookup_field = 'id'
#
#
#     def get(self,request,id=None):
#         if id:
#             return self.retrieve(request,id)
#         else:
#             return self.list(request)
#
#
#     def post(self,request):
#         return self.create(request)
#
#     def put(self,request,id):
#         return self.update(request,id)
#
#     def delete(self,request,id):
#         return self.delete(request,id)
#
#
#
# class DivViewSet(viewsets.ModelViewSet):
#     serializer_class = DivSerializer
#
#     def get_queryset(self):
#         qury = DivModel.objects.all()
#         return qury
#
#
# class AutheView(generics.GenericAPIView,mixins.ListModelMixin):
#     serializer_class = AutheSerializer
#     queryset = User.objects.all()
#
#     def get(self,request):
#         return self.list(request)
#
#     def post(self, request):
#         serializer = AutheSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.errors, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
