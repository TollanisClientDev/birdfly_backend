# app/routes/uploads.py
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi import Depends
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError
from app.database.mongo import mongo_db  # adjust to your project
from typing import Optional

router = APIRouter(prefix="/uploads", tags=["Uploads"])

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # default if missing
s3 = boto3.client("s3", region_name=AWS_REGION)

def _make_s3_key(user_id: str, filename: str):
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    safe_filename = filename.replace(" ", "_")  # basic sanitize
    return f"drivers/{user_id}/{ts}_{safe_filename}"

@router.get("/presign")
def presign_put_url(
    user_id: str = Query(...),
    filename: str = Query(...),
    content_type: str = Query(...),
    expires_in: Optional[int] = Query(300)
):
    if not S3_BUCKET:
        raise HTTPException(status_code=500, detail="S3_BUCKET not configured")
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
        raise HTTPException(status_code=500, detail=str(e))
    return {"url": url, "key": key, "bucket": S3_BUCKET}

class ConfirmIn(BaseModel):
    user_id: str
    key: str
    doc_type: Optional[str] = "other"

@router.post("/confirm")
def confirm_upload(payload: ConfirmIn):
    # verify object exists and read metadata
    try:
        head = s3.head_object(Bucket=S3_BUCKET, Key=payload.key)
    except ClientError as e:
        raise HTTPException(status_code=400, detail="Object not found in S3")
    # store metadata in Mongo
    doc = {
        "user_id": payload.user_id,
        "doc_type": payload.doc_type,
        "s3_key": payload.key,
        "bucket": S3_BUCKET,
        "content_type": head.get("ContentType"),
        "size": head.get("ContentLength"),
        "uploaded_at": datetime.utcnow(),
        "verified": False
    }
    mongo_db.driver_documents.insert_one(doc)
    return {"ok": True, "doc": {"key": payload.key}}
