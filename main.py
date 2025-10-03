from creds.init_creds import init_credentials
init_credentials()
from fastapi import FastAPI
from routers import releases

app = FastAPI(title="GitHub Releases CRUD API")
app.include_router(releases.router, prefix="/releases", tags=["releases"])
