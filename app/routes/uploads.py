# app/routes/uploads.py
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

# Adjust this import to your project's mongo client wrapper
# It should expose a `mongo_db` object (pymongo Database)
from app.database.mongo import mongo_db

router = APIRouter(prefix="/uploads", tags=["Uploads"])

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", None)  # e.g. "ap-south-1"
MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # default 10 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "application/pdf"}

# Initialize boto3 client (will use IAM role if running on EC2 with role attached)
if AWS_REGION:
    s3 = boto3.client("s3", region_name=AWS_REGION)
else:
    s3 = boto3.client("s3")


def _sanitize_filename(name: str) -> str:
    return name.replace(" ", "_").replace("/", "_")


def _make_s3_key(user_id: str, filename: str) -> str:
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    safe = _sanitize_filename(filename)
    return f"drivers/{user_id}/{ts}_{safe}"


class ConfirmIn(BaseModel):
    user_id: str
    key: str
    doc_type: Optional[str] = "other"


@router.get("/presign")
def presign_put_url(
    user_id: str = Query(...),
    filename: str = Query(...),
    content_type: str = Query(...),
    expires_in: Optional[int] = Query(300)
):
    """
    Returns a presigned PUT URL and the S3 key. Frontend should PUT directly to the returned URL.
    """
    if not S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET not configured on server")

    # Basic validation
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Content type not allowed")

    key = _make_s3_key(user_id, filename)

    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": key,
                "ContentType": content_type,
                "ACL": "private"
            },
            ExpiresIn=expires_in
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"s3 error: {str(e)}")

    return {"url": url, "key": key, "bucket": S3_BUCKET}


@router.post("/confirm")
def confirm_upload(payload: ConfirmIn):
    """
    After frontend PUTs to the presigned URL, call this to verify the object exists and save metadata in Mongo.
    """
    if not S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET not configured")

    # Verify object exists and fetch metadata with head_object
    try:
        head = s3.head_object(Bucket=S3_BUCKET, Key=payload.key)
    except ClientError as e:
        raise HTTPException(status_code=400, detail="Object not found in S3 or access denied")

    size = head.get("ContentLength", 0)
    content_type = head.get("ContentType", "")

    # Optional server-side validations
    if size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File too large")

    # Save metadata in Mongo (collection: driver_documents)
    doc = {
        "user_id": payload.user_id,
        "doc_type": payload.doc_type,
        "s3_key": payload.key,
        "bucket": S3_BUCKET,
        "content_type": content_type,
        "size": size,
        "uploaded_at": datetime.utcnow(),
        "verified": False
    }
    res = mongo_db.driver_documents.insert_one(doc)
    return {"ok": True, "doc_id": str(res.inserted_id), "key": payload.key}


@router.post("/upload-proxy")
async def upload_proxy(user_id: str, file: UploadFile = File(...)):
    """
    Backend-proxied upload: client POSTs file to this endpoint; backend uploads to S3.
    Simpler for clients that can't do presigned PUTs (e.g., some RN setups).
    """
    if not S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET not configured")

    # Basic content-type validation
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Content type not allowed")

    # Optionally check file size by reading file.file (stream). Here we trust client but can check:
    # file.file.seek(0, 2); size = file.file.tell(); file.file.seek(0)
    # For safety, stream upload with upload_fileobj and don't load into memory.

    key = _make_s3_key(user_id, file.filename)

    try:
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=S3_BUCKET,
            Key=key,
            ExtraArgs={"ContentType": file.content_type, "ACL": "private"}
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"upload failed: {str(e)}")
    finally:
        try:
            file.file.close()
        except Exception:
            pass

    # Save metadata in Mongo
    doc = {
        "user_id": user_id,
        "doc_type": "unknown",
        "s3_key": key,
        "bucket": S3_BUCKET,
        "content_type": file.content_type,
        "size": None,
        "uploaded_at": datetime.utcnow(),
        "verified": False
    }
    res = mongo_db.driver_documents.insert_one(doc)
    return {"ok": True, "key": key, "doc_id": str(res.inserted_id)}


@router.get("/download-presign")
def presign_get_url(key: str = Query(...), expires_in: Optional[int] = Query(60)):
    """
    Generate a presigned GET URL to allow temporary downloads of private objects.
    """
    if not S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET not configured")
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": S3_BUCKET, "Key": key},
            ExpiresIn=expires_in
        )
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"url": url}
