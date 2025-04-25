from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CreateUserDto:
    name: str
    email: str

@dataclass
class UpdateUserDto:
    name: Optional[str] = None
    email: Optional[str] = None
