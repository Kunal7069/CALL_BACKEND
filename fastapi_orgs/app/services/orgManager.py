from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.models.orgModel import Organization
from app.utils.csv_parser import parse_csv_files

class OrganizationManager:
    def __init__(self, db: Session):
        self.db = db

    async def create(
        self,
        name: str,
        category: str,
        parameters: str,
        email: str,
        files: List[UploadFile]
    ) -> Organization:
        try:
            # Parse CSV files into description dictionary
            description = await parse_csv_files(files)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV files: {str(e)}")

        try:
            org = Organization(
                name=name,
                category=category,
                parameters=parameters,
                email=email,
                description=description
            )

            self.db.add(org)
            self.db.commit()
            self.db.refresh(org)
            return org

        except SQLAlchemyError as db_err:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_err)}")

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
    def get_by_name(self, name: str) -> Organization:
        try:
            org = self.db.query(Organization).filter(Organization.name == name).first()
            if not org:
                raise HTTPException(status_code=404, detail=f"Organization with name '{name}' not found")
            return org
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching organization: {str(e)}")
        
        
    def get_by_id(self, org_id: UUID) -> Organization:
        try:
            org = self.db.query(Organization).filter(Organization.id == org_id).first()
            if not org:
                raise HTTPException(status_code=404, detail=f"Organization with ID '{org_id}' not found")
            return org
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching organization by ID: {str(e)}")