from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apiv1 import routes_v1
from settings import settings

app = FastAPI()


app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
)
app.include_router(routes_v1.router)

# async start
