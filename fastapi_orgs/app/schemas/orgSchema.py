import uuid
from typing import Dict

from pydantic import BaseModel, EmailStr


class OrgBase(BaseModel):
    name: str
    category: str
    parameters: str
    email: EmailStr


class OrgCreate(OrgBase):
    pass


class OrgResponse(OrgBase):
    id: uuid.UUID
    description: Dict[str, list]

    class Config:
        orm_mode = True
