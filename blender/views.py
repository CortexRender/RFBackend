import os

from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from utils.response import RFResponse, ResponseCodes

TEMP_DIR = os.path.join(settings.BASE_DIR, "files")  # Temporary directory for files
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure temp directory exists

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    file_obj = request.FILES.get("file")
    if not file_obj:
        return RFResponse(code=ResponseCodes.BAD_REQUEST, message="No file uploaded")

    # file_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)
    # with open(file_path, "wb+") as destination:
    #     for chunk in file_obj.chunks():
    #         destination.write(chunk)
    temp_file_path = os.path.join(TEMP_DIR, file_obj.name)
    with open(temp_file_path, "wb+") as temp_file:
        for chunk in file_obj.chunks():
            temp_file.write(chunk)

    return RFResponse(code=ResponseCodes.CREATED, message="File uploaded successfully", data={"file_name": file_obj.name})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_file(request, file_name):
    # file_path = os.path.join(TEMP_DIR, "blended", file_name)
    file_path = os.path.join(TEMP_DIR, file_name)
    print(file_path)
    # if os.path.exists(file_path):
    #     return FileResponse(open(file_path, "rb"), as_attachment=True)
    #
    # return RFResponse(code=ResponseCodes.NOT_FOUND, message="File not found")
    if not os.path.exists(file_path):
        return RFResponse(code=ResponseCodes.NOT_FOUND, message="File not found")

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk

    response = StreamingHttpResponse(file_iterator(file_path), content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response