import jwt
import os
from datetime import datetime, timezone
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class InvalidTokenException(Exception):
    pass


def get_email_from_token(token: str) -> str:
    try:
        if '.' not in token or token.count('.') != 2:
            raise InvalidTokenException("Token is not in JWT format. Received a session token instead of JWT.")
        
        secret = os.getenv("JWT_SECRET") or os.getenv("AUTH_SECRET")
        if not secret:
            raise InvalidTokenException("JWT_SECRET or AUTH_SECRET not configured")
        
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        
        email = payload.get("email")
        if not email:
            raise InvalidTokenException("Email not found in token payload")
        
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise InvalidTokenException("Token has expired")
        
        return email
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError as e:
        raise InvalidTokenException(f"Invalid or expired token: {str(e)}")
    except Exception as e:
        raise InvalidTokenException(f"Token validation failed: {str(e)}")


def decode_jwt_token(token: str) -> dict:
    try:
        if '.' not in token or token.count('.') != 2:
            raise InvalidTokenException("Token is not in JWT format")
        
        secret = os.getenv("BETTER_AUTH_SECRET") or os.getenv("AUTH_SECRET")
        if not secret:
            raise InvalidTokenException("JWT_SECRET or AUTH_SECRET not configured")
        
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError as e:
        raise InvalidTokenException(f"Invalid or expired token: {str(e)}")
    except Exception as e:
        raise InvalidTokenException(f"Token validation failed: {str(e)}")