from __future__ import annotations
import re
from uuid import uuid4
from datetime import datetime, timezone
from typing import Any, Dict

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.settings import settings

def s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )

def _safe_filename(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_.")
    return name or "file"

def build_s3_key(filename: str) -> str:
    safe = _safe_filename(filename)
    date_path = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    base = f"{date_path}/{uuid4().hex}_{safe}"
    prefix = settings.S3_PREFIX.strip("/")
    return f"{prefix}/{base}" if prefix else base

def create_presigned_put_url(*, key: str, content_type: str) -> str:
    client = s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
            "ContentType": content_type,
            "ServerSideEncryption": "AES256"
        },
        ExpiresIn=settings.PRESIGN_PUT_EXPIRES,
        HttpMethod="PUT",
    )


def create_presigned_post(*, filename: str, content_type: str, max_size_bytes: int) -> Dict[str, Any]:
    key = build_s3_key(filename)
    client = s3_client()

    fields = {
        "Content-Type": content_type,
        "x-amz-server-side-encryption": "AES256"
    }

    conditions = [
        {"Content-Type": content_type},
        {"x-amz-server-side-encryption": "AES256"},
        ["content-length-range", 1, max_size_bytes],
    ]

    prefix = settings.S3_PREFIX.strip("/")
    if prefix:
        conditions.append(["starts-with", "$key", f"{prefix}/"])

    resp = client.generate_presigned_post(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=settings.PRESIGN_PUT_EXPIRES,
    )
    return {"key": key, **resp}


def create_presigned_get_url(*, key: str, expires_in: int | None = None,
                             download_name: str | None = None,
                             content_type: str | None = None) -> str:
    client = s3_client()
    params = {"Bucket": settings.S3_BUCKET, "Key": key}
    if download_name:
        params["ResponseContentDisposition"] = f'attachment; filename="{download_name}"'
    if content_type:
        params["ResponseContentType"] = content_type
    return client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=expires_in or settings.PRESIGN_GET_EXPIRES,
    )


def head_object(key: str) -> Dict[str, Any] | None:
    client = s3_client()
    try:
        return client.head_object(Bucket=settings.S3_BUCKET, Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
            return None
        raise

def health_s3() -> bool:
    try:
        s3_client().head_bucket(Bucket=settings.S3_BUCKET)
        return True
    except Exception:
        return False
