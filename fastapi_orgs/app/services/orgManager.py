from typing import List
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi_orgs.app.models.orgModel import Organization
from fastapi_orgs.app.utils.csv_parser import parse_csv_files


class OrganizationManager:
    def __init__(self, db: Session):
        """
        Initialize OrganizationManager with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    async def create(
        self,
        name: str,
        category: str,
        parameters: str,
        email: str,
        files: List[UploadFile],
    ) -> Organization:
        """
        Create a new organization entry in the database.

        This method also parses the uploaded CSV files to generate a description
        JSON which is saved with the organization record.

        Args:
            name (str): Name of the organization.
            category (str): Category of the organization.
            parameters (str): Parameters associated with the organization.
            email (str): Contact email for the organization.
            files (List[UploadFile]): List of uploaded CSV files.

        Returns:
            Organization: The created organization object.

        Raises:
            HTTPException: If CSV parsing fails or database operations fail.
        """
        try:
            # Parse CSV files into description dictionary
            description = await parse_csv_files(files)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error parsing CSV files: {str(e)}"
            )

        try:
            org = Organization(
                name=name,
                category=category,
                parameters=parameters,
                email=email,
                description=description,
            )

            self.db.add(org)
            self.db.commit()
            self.db.refresh(org)
            return org

        except SQLAlchemyError as db_err:
            self.db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(db_err)}"
            )

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_by_name(self, name: str) -> Organization:
        """
        Retrieve an organization by its name.

        Args:
            name (str): The name of the organization.

        Returns:
            Organization: The organization object if found.

        Raises:
            HTTPException: If the organization is not found or query fails.
        """
        try:
            org = self.db.query(Organization).filter(Organization.name == name).first()
            if not org:
                raise HTTPException(
                    status_code=404, detail=f"Organization with name '{name}' not found"
                )
            return org
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching organization: {str(e)}"
            )

    def get_by_id(self, org_id: UUID) -> Organization:
        """
        Retrieve an organization by its unique UUID.

        Args:
            org_id (UUID): UUID of the organization.

        Returns:
            Organization: The organization object if found.

        Raises:
            HTTPException: If the organization is not found or query fails.
        """
        try:
            org = self.db.query(Organization).filter(Organization.id == org_id).first()
            if not org:
                raise HTTPException(
                    status_code=404, detail=f"Organization with ID '{org_id}' not found"
                )
            return org
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching organization by ID: {str(e)}"
            )
