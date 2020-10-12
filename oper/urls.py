# from django.urls import path,include
# from .views import *
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('div', DivViewSet, basename='diver')
#
#
# urlpatterns=[
#     path('class/', ClassListView.as_view()),
#     # path('admin/', AdminListView.as_view()),
#     path('division/', DivListView.as_view()),
#     path('division/<int:id>', DivListView.as_view()),
#     path('', include(router.urls)),
#     path('login/', AutheView.as_view()),
# ]



from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^login/$',
        views.UserLoginAPIView.as_view(),
        name='login'),

    url(r'^register/$',
        views.UserRegistrationAPIView.as_view(),
        name='register'),

    url(r'^verify/(?P<verification_key>.+)/$',
        views.UserEmailVerificationAPIView.as_view(),
        name='email_verify'),

    url(r'^password_reset/$',
        views.PasswordResetAPIView.as_view(),
        name='password_change'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

    url(r'^user-profile/$',
        views.UserProfileAPIView.as_view(),
        name='user_profile'),


]
