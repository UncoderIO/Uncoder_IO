import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.assistance import assistance_router, lifespan
from app.routers.ioc_translate import iocs_router
from app.routers.translate import st_router

app = FastAPI(title="Siem Converter API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(st_router)
app.include_router(iocs_router)
app.include_router(assistance_router)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", "8000")
    if not port.isnumeric():
        raise Exception("Port should be a number!")
    uvicorn.run(app, host=host, port=int(port))
