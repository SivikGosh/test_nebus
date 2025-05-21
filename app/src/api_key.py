from fastapi import Header, HTTPException, status
import os

SECRET_KEY = os.getenv('SECRET_KEY', '1qazxsw2')


def verify_secret_key(x_api_key: str = Header(..., alias='X-API-Key')):
    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
