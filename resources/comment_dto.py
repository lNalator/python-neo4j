from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateCommentDto:
    user_id: int
    content: str

@dataclass
class UpdateCommentDto:
    content: Optional[str] = None
