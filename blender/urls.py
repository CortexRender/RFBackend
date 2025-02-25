from django.urls import path
from .views import upload_file, download_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", upload_file, name="upload_file"),
    path("download/<str:file_name>/", download_file, name="download_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
