from fastapi import FastAPI
from fastapi_injector import attach_injector
from injector import Injector

from packages.web import routes


def create_fastapi_app(injector: Injector):
    app = FastAPI()
    app.include_router(routes.jobs.index.router)
    attach_injector(app, injector)
    return app

