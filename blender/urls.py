from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import initiate_multipart_upload, complete_multipart_upload, \
    generate_presigned_urls, delete_file

urlpatterns = [
    path("upload/initiate/", initiate_multipart_upload, name="initiate_upload"),
    path("upload/presigned-urls/", generate_presigned_urls, name="generate_presigned_urls"),
    path("upload/complete/", complete_multipart_upload, name="complete_upload"),
    path("delete/", delete_file, name="delete_file"),
    # path("download/<str:file_name>/", download_file, name="download_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
