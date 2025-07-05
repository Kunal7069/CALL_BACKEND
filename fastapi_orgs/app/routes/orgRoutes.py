
from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List, Annotated
from sqlalchemy.orm import Session

from app.schemas.orgSchema import OrgResponse
from app.services.orgManager import OrganizationManager
from app.config.database import get_db

router = APIRouter()

@router.post("/organizations/", response_model=OrgResponse)
async def create_organization(
    files: Annotated[List[UploadFile],File(description="Upload one or more CSV files")],
    name: str = Form(...),
    category: str = Form(...),
    parameters: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    manager = OrganizationManager(db)
    org = await manager.create(name, category, parameters, email, files)
    return org


@router.get("/organizations/{name}", response_model=OrgResponse)
def get_organization_by_name(name: str, db: Session = Depends(get_db)):
    manager = OrganizationManager(db)
    org = manager.get_by_name(name)
    return org