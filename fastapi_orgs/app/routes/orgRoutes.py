from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from fastapi_orgs.app.config.database import get_db
from fastapi_orgs.app.schemas.orgSchema import OrgResponse
from fastapi_orgs.app.services.orgManager import OrganizationManager
from fastapi_orgs.app.settings import ORG_ROUTES

router = APIRouter()


@router.post(ORG_ROUTES["create"], response_model=OrgResponse)
async def create_organization(
    files: Annotated[
        List[UploadFile], File(description="Upload one or more CSV files")
    ],
    name: str = Form(...),
    category: str = Form(...),
    parameters: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    manager = OrganizationManager(db)
    org = await manager.create(name, category, parameters, email, files)
    return org


@router.get(ORG_ROUTES["get_by_name"], response_model=OrgResponse)
def get_organization_by_name(name: str, db: Session = Depends(get_db)):
    manager = OrganizationManager(db)
    org = manager.get_by_name(name)
    return org
