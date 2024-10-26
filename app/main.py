from fastapi import FastAPI

# From arquivo routes que está dentro da pasta router, importar a instância router
from router.routes import router

app = FastAPI()

app.include_router(router)