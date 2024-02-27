
from fastapi import FastAPI
from .endpoints import router

def create_app() -> FastAPI:

    app = FastAPI(debug=False)

    app.include_router(router=router)

    return app