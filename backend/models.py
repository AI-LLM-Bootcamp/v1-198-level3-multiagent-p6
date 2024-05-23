from typing import List
from pydantic import BaseModel


class NamedUrl(BaseModel):
    name: str
    url: str


class BusinessareaInfo(BaseModel):
    technology: str
    businessarea: str
    blog_articles_urls: List[str]
    youtube_videos_urls: List[NamedUrl]


class BusinessareaInfoList(BaseModel):
    businessareas: List[BusinessareaInfo]