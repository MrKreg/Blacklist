from django.urls import path
from rest_framework import routers

from app.pkg.domains.api import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'blacklist', views.BlockedDomainsViewSet, 'blacklist')
router.register(r'requests/review', views.RequestReviewViewSet, 'review')

urlpatterns = [
    path('block', views.DomainBlockRequestView.as_view(), name='block_request'),
]

urlpatterns = urlpatterns + router.urls
