import os
import uuid
import cloudinary
import cloudinary.uploader
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from rest_framework.response import Response

load_dotenv()
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True
)

# Initialize Azure client
account_url = "https://usalamawangu.blob.core.windows.net"
container_name = "usalama-wangu-audio"

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    print("⚠️ Missing AZURE_STORAGE_CONNECTION_STRING — Azure upload disabled.")
else:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def upload_audio(audio_file):
    """
    Uploads an audio file to Azure Blob Storage and Cloudinary (as fallback or duplicate).
    Returns URLs for both (if successful).
    """
    azure_url = None
    cloudinary_url = None

    if hasattr(audio_file, "name"):  # Django or file-like object
        file_name = audio_file.name
        file_obj = audio_file
    else:  # string path
        file_name = os.path.basename(audio_file)
        file_obj = open(audio_file, "rb")

    # Generate a unique filename
    file_ext = os.path.splitext(file_name)[1]
    blob_name = f"{uuid.uuid4()}{file_ext}"

    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(file_obj, overwrite=True)
        azure_url = f"{account_url}/{container_name}/{blob_name}"
        print(f"Uploaded to Azure: {azure_url}")
    except Exception as e:
        print(f"Azure upload failed: {e}")


    # Resetting the file pointer for Cloudinary
    if hasattr(file_obj, "seek"):
        try:
            file_obj.seek(0)
        except Exception:
            pass

    try:
        upload_response = cloudinary.uploader.upload(
            file_obj,
            folder="Usalama_wangu_emergency_audio",
            resource_type="video"
        )
        cloudinary_url = upload_response["secure_url"]
        print(f"Uploaded to Cloudinary: {cloudinary_url}")

    except Exception as e:
        print(f"Cloudinary upload failed: {e}")

    if not azure_url and not cloudinary_url:
        return Response({'error': 'Both Azure and Cloudinary uploads failed'}, status=500)

    return azure_url, cloudinary_url
