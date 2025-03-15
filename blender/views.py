import logging
import os

import boto3
import botocore
from django.conf import settings
from django.http import StreamingHttpResponse, FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.response import RFResponse, ResponseCodes

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
    config=botocore.config.Config(signature_version="s3v4"),
)


### Step 1: Initiate Multipart Upload
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_multipart_upload(request):
    file_name = request.data.get("file_name")
    username = request.user.username

    if not file_name:
        return RFResponse(code=ResponseCodes.BAD_REQUEST, message="File name is required")

    try:
        response = s3_client.create_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"fileUpload/{username}/{file_name}",
        )

        return RFResponse(
            code=ResponseCodes.SUCCESS,
            message="Multipart upload initiated",
            data={"upload_id": response["UploadId"], "file_name": file_name},
        )

    except Exception as e:
        return RFResponse(
            code=ResponseCodes.INTERNAL_SERVER_ERROR,
            message="Failed to initiate multipart upload",
            errors=str(e),
        )


### Step 2: Generate Pre-Signed URLs for Each Chunk
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_presigned_urls(request):
    username = request.user.username
    file_name = request.data.get("file_name")
    upload_id = request.data.get("upload_id")
    part_numbers = request.data.get("part_numbers")  # List of part numbers [1,2,3...]

    if not file_name or not upload_id or not part_numbers:
        return RFResponse(code=ResponseCodes.BAD_REQUEST, message="Missing required parameters")

    try:
        presigned_urls = {}

        for part_number in part_numbers:
            url = s3_client.generate_presigned_url(
                "upload_part",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": f"fileUpload/{username}/{file_name}",
                    "UploadId": upload_id,
                    "PartNumber": part_number,
                },
                ExpiresIn=3600 * 2,
            )
            presigned_urls[str(part_number)] = url

        return RFResponse(
            code=ResponseCodes.SUCCESS,
            message="Pre-signed URLs generated",
            data={"presigned_urls": presigned_urls},
        )

    except Exception as e:
        return RFResponse(
            code=ResponseCodes.INTERNAL_SERVER_ERROR,
            message="Failed to generate pre-signed URLs",
            errors=str(e),
        )


### Step 3: Complete Multipart Upload
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_multipart_upload(request):
    username = request.user.username
    file_name = request.data.get("file_name")
    upload_id = request.data.get("upload_id")
    parts = request.data.get("parts")  # List of {'ETag': 'etag_value', 'PartNumber': num}

    if not file_name or not upload_id or not parts:
        return RFResponse(code=ResponseCodes.BAD_REQUEST, message="Missing required parameters")

    try:
        response = s3_client.complete_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"fileUpload/{username}/{file_name}",
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

        return RFResponse(
            code=ResponseCodes.SUCCESS,
            message="Multipart upload completed",
            data={"file_url": response["Location"]},
        )

    except Exception as e:
        return RFResponse(
            code=ResponseCodes.INTERNAL_SERVER_ERROR,
            message="Failed to complete multipart upload",
            errors=str(e),
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_file(request):
    username = request.user.username
    file_name = request.data.get("file_name")

    if not file_name:
        return RFResponse(code=ResponseCodes.BAD_REQUEST, message="File name is required")

    try:
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"fileUpload/{username}/{file_name}")

        return RFResponse(
            code=ResponseCodes.SUCCESS,
            message="File deleted successfully",
        )

    except Exception as e:
        return RFResponse(
            code=ResponseCodes.INTERNAL_SERVER_ERROR,
            message="Failed to delete file",
            errors=str(e),
        )
