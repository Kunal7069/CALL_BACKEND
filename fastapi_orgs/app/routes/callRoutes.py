from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_orgs.app.config.database import get_db
from fastapi_orgs.app.services.callManager import CallManager
from fastapi_orgs.app.services.orgManager import OrganizationManager
from fastapi_orgs.app.settings import CALL_ROUTES
from fastapi_orgs.app.utils.sambanova import SambaNovaService

router = APIRouter()

call_mgr = CallManager()
sambanova_service = SambaNovaService()


@router.post(CALL_ROUTES["initiate"])
def initiate_call(org_id: str = Body(...), phone_number: str = Body(...)):
    try:
        call_id = call_mgr.initiate_call(org_id, phone_number)
        return {"call_id": call_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(CALL_ROUTES["keys"])
async def get_keys(call_id: str, db: Session = Depends(get_db)):
    try:
        manager = OrganizationManager(db)
        org_id = call_mgr.call_sessions[call_id]["org_id"]
        org = manager.get_by_id(org_id)
        description = org.description
        keys_list = list(description.keys())
        return keys_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(CALL_ROUTES["message"])
async def record_message(
    call_id: str,
    question: str = Body(...),
    selected_sources: List[str] = Body(...),
    db: Session = Depends(get_db),
):
    try:
        manager = OrganizationManager(db)
        org_id = call_mgr.call_sessions[call_id]["org_id"]
        org = manager.get_by_id(org_id)
        description = org.description
        filtered_description = {
            key: value for key, value in description.items() if key in selected_sources
        }
        answer = await sambanova_service.ask_question(
            description=filtered_description, question=question
        )
        call_mgr.add_message(call_id, question, answer)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(CALL_ROUTES["end"])
async def end_call(call_id: str):
    try:
        session = call_mgr.end_call(call_id)
        summary = await sambanova_service.extract_summary(
            session
        )  # sends whole data to SambaNova
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
