from pydantic import BaseModel, EmailStr
from typing import Dict
import uuid

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