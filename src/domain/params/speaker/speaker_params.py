from typing import Optional
import uuid

from fastapi import Form


class SpeakerParams:
    class Create:
        name: str
        title: str
        social_media_links: str
        company: str

        def __init__(self, name: str, title: str, social_media_links: str, company: str):
            self.name = name
            self.title = title
            self.social_media_links = social_media_links
            self.company = company

        @classmethod
        def as_form(
                cls,
                name: str = Form(..., description="Speaker name"),
                title: str = Form(..., description="Judul Materi"),
                social_media_links: str = Form(..., description="Link Sosial"),
                company: str = Form(..., description="Perusahaan")
        ):
            return cls(
                name=name,
                title=title,
                social_media_links=social_media_links,
                company=company
            )

    class Update:
        name: Optional[str]
        title: Optional[str]
        social_media_links: Optional[str]
        company: Optional[str]

        def __init__(
                self,
                name: Optional[str],
                title: Optional[str],
                social_media_links: Optional[str], 
                company: Optional[str]
        ):
            self.name = name
            self.title = title
            self.social_media_links = social_media_links
            self.company = company

        @classmethod
        def as_form(
                cls,
                name: Optional[str] = Form(None, description="Speaker name"),
                title: Optional[str] = Form(None, description="Judul Materi"),
                social_media_links: Optional[str] = Form(None, description="Link Sosial"),
                company: Optional[str] = Form(None, description="Perusahaan")
        ):
            return cls(
                name=name,
                title=title,
                social_media_links=social_media_links,
                company=company
            )

    class Get:
        def __init__(
                self, 
                parameter: Optional[str],
                page: int = 1,
                page_size: int = 10
        ):
            self.parameter = parameter
            self.page = page
            self.page_size = page_size

    class Find:
        def __init__(
                self,
                speaker_id: uuid.UUID | str,
            ):
            self.speaker_id = speaker_id

    class Delete:
        def __init__(self, speaker_id: str | uuid.UUID):
            self.speaker_id = speaker_id
