from fastapi import FastAPI

from apiv1 import routes_v1

app = FastAPI()

app.include_router(routes_v1.router)
