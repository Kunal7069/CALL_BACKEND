from fastapi import APIRouter, HTTPException, Body, Depends
from app.services.callManager import CallManager
from app.services.orgManager import OrganizationManager
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.sambanova import ask_sambanova, extract_summary
# from app.services.callManager import CallManager, call_sessions
from app.services.callManager import CallManager
router = APIRouter()
call_mgr = CallManager()

@router.post("/calls/initiate")
def initiate_call(org_id: str = Body(...), phone_number: str = Body(...)):
    try:
        call_id = call_mgr.initiate_call(org_id, phone_number)
        return {"call_id": call_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calls/{call_id}/message")
async def record_message(call_id: str, question: str = Body(...), db: Session = Depends(get_db)):
    try:
        manager = OrganizationManager(db)
        org_id = call_mgr.call_sessions[call_id]["org_id"]  # ✅ fixed access
        org = manager.get_by_id(org_id)
        description = org.description

        answer = await ask_sambanova(description, question)
        call_mgr.add_message(call_id, question, answer)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/calls/{call_id}/end")
async def end_call(call_id: str):
    try:
        session = call_mgr.end_call(call_id)
        summary = await extract_summary(session)  # sends whole data to SambaNova
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
