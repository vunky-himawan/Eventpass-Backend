import os
from datetime import datetime, timedelta
from domain.entities.user.user import User
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer
from domain.entities.organization_member.organization_member import OrganizationMember
from fastapi.exceptions import HTTPException
import json
import logging  

class JWTTokenService:
    def __init__(self):
        self.JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
        self.JWT_REFRESH_SECRET_KEY = str(os.getenv("JWT_REFRESH_SECRET_KEY"))
        self.ALGORITHM = str(os.getenv("ALGORITHM", "HS256"))
        
        # Parse access and refresh token expiration times
        self.ACCESS_TOKEN_EXPIRE = self._parse_expiration_time(os.getenv("ACCESS_TOKEN_EXPIRE", "30h"))
        self.REFRESH_TOKEN_EXPIRE = self._parse_expiration_time(os.getenv("REFRESH_TOKEN_EXPIRE", "3d"))

    def create_access_token(self, user: User, event_id: str | None = None) -> str:
        expire = datetime.now() + self.ACCESS_TOKEN_EXPIRE

        to_encode = {
            "exp": expire,
            "sub": str(user.user_id),
        }

        if event_id is not None:
            to_encode["event_id"] = event_id
    
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user: User, event_id: str | None = None) -> str:
        expire = datetime.now() + self.REFRESH_TOKEN_EXPIRE

        to_encode = {
            "exp": expire,
            "sub": str(user.user_id),
        }

        if event_id is not None:
            to_encode["event_id"] = event_id
        
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        try:
            token = str(token)

            payload = jwt.decode(
                token, 
                self.JWT_SECRET_KEY, 
                algorithms=[self.ALGORITHM],
            )

            return payload
        except ExpiredSignatureError as e:
            return HTTPException(status_code=401, detail="Token expired")
        except JWTError as e:
            return HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            return HTTPException(status_code=401, detail="Invalid token")
        
    def verify_refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except Exception as e:
            return HTTPException(status_code=401, detail="Invalid token")
    
    def _parse_expiration_time(self, expiration: str) -> timedelta:
        """Parse the expiration time from environment variable format (e.g., '30h', '3d') to timedelta."""
        try:
            if expiration.endswith("h"):
                return timedelta(hours=int(expiration[:-1]))
            elif expiration.endswith("d"):
                return timedelta(days=int(expiration[:-1]))
            else:
                raise ValueError("Unsupported expiration format. Use 'h' for hours or 'd' for days.")
        except Exception as e:
            print(f"Error parsing expiration time: {e}")
            return timedelta(hours=1)  # Default to 1 hour if there's an error
