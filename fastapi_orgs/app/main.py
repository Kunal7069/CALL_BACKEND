from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_orgs.app.config.database import engine
from fastapi_orgs.app.models.orgModel import Base
from fastapi_orgs.app.routes import callRoutes, orgRoutes

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Organization API", version="1.0")

# Optional: CORS settings for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(orgRoutes.router, prefix="/api", tags=["Organizations"])
app.include_router(callRoutes.router, prefix="/api", tags=["Calls"])
