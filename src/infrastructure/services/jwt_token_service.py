import os
from datetime import datetime, timedelta
from domain.entities.user.user import User
from jose import jwt
from domain.entities.participant.participant import Participant
from domain.entities.event_organizer.event_organizer import EventOrganizer

class JWTTokenService:
    def __init__(self):
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        self.JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        
        # Parse access and refresh token expiration times
        self.ACCESS_TOKEN_EXPIRE = self._parse_expiration_time(os.getenv("ACCESS_TOKEN_EXPIRE", "30h"))
        self.REFRESH_TOKEN_EXPIRE = self._parse_expiration_time(os.getenv("REFRESH_TOKEN_EXPIRE", "3d"))

    def create_access_token(self, user: User, details: Participant | EventOrganizer | None = None) -> str:
        expire = datetime.now() + self.ACCESS_TOKEN_EXPIRE
        to_encode = {
            "exp": expire,
            "sub": {
                "id": str(user.user_id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }
    
        # Hanya tambahkan `details` jika tidak bernilai None
        if details is not None and isinstance(details, Participant):
            to_encode["sub"]["participant_name"] = details.participant_name
        elif details is not None and isinstance(details, EventOrganizer):
            to_encode["sub"]["organization_name"] = details.organization_name
    
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user: User, details: Participant | EventOrganizer | None = None) -> str:
        expire = datetime.now() + self.REFRESH_TOKEN_EXPIRE
        to_encode = {
            "exp": expire,
            "sub": {
                "id": str(user.user_id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }

        if details is not None and isinstance(details, Participant):
            to_encode["sub"]["participant_name"] = details.participant_name
        elif details is not None and isinstance(details, EventOrganizer):
            to_encode["sub"]["organization_name"] = details.organization_name
        
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_access_token(self, token: str, user: User) -> bool:
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload["sub"] == str(user.id)
        except Exception as e:
            print(f"Error verifying access token: {e}")
            return False
    
    def verify_refresh_token(self, token: str, user: User) -> bool:
        try:
            payload = jwt.decode(token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload["sub"] == str(user.id)
        except Exception as e:
            print(f"Error verifying refresh token: {e}")
            return False
    
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
