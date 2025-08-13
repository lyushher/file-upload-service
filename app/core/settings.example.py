from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "file-upload-service-core"
    API_KEY: str = None

    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    AWS_REGION: str = None
    S3_BUCKET: str = None

    S3_PREFIX: str = ""
    PRESIGN_PUT_EXPIRES: int = 900
    PRESIGN_GET_EXPIRES: int = 300

    ALLOWED_ORIGINS: str = "http://localhost:3000"
    ALLOWED_CONTENT_TYPES: str = "text/plain,image/png,image/jpeg,application/pdf"
    MAX_UPLOAD_MB: int = 25

    POSTGRES_USER: str = "youruser"
    POSTGRES_PASSWORD: str = "yourpassword"
    POSTGRES_DB: str = "file_upload_service"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    class Config:
        env_file = ".env"

    @property
    def allowed_mime_set(self) -> set[str]:
        return {t.strip() for t in self.ALLOWED_CONTENT_TYPES.split(",") if t.strip()}

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_MB * 1024 * 1024
