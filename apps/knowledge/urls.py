from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, KnowledgeBaseViewSet

router = DefaultRouter()
router.register(r'knowledge-bases', KnowledgeBaseViewSet, basename='knowledgebase')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]
