from dataclasses import dataclass
from typing import Optional

@dataclass
class CreatePostDto:
    title: str
    content: str

@dataclass
class UpdatePostDto:
    title: Optional[str] = None
    content: Optional[str] = None
