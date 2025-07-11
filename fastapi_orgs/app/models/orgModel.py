import uuid

from sqlalchemy import JSON, Column, String
from sqlalchemy.dialects.postgresql import UUID

from fastapi_orgs.app.config.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    parameters = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    description = Column(JSON, nullable=False)
