from rest_framework import routers
from app.views import UserRegesterViewSet, UserLoginViewSet, UserLogoutViewSet, UserProfileViewSet
from django.conf.urls import url, include


router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    url(r'^create/$', UserRegesterViewSet.as_view(), name='create'),
    url(r'^login/$', UserLoginViewSet.as_view(), name='login'),
    url(r'^logout/$', UserLogoutViewSet.as_view(), name='logout'),
    url(r'^', include(router.urls))

]