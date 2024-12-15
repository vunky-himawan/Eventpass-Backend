from fastapi import Form
from pydantic import BaseModel

class LogoutRequest(BaseModel):
    refresh_token: str

    @classmethod
    async def as_form(
        cls,
        refresh_token: str = Form(...),
    ):
        return cls(
            refresh_token=refresh_token,
        )