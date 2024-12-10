from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from database import create_db_and_tables
from routes import router

tags_metadata = [
    {
        "name": "Students",
        "description": "Operations with students.",
    },
    {
        "name": "Groups",
        "description": "Operations with groups.",
    },
]

app = FastAPI(title="StudentGroup_App",
    description="You can implement various operations through the API",
    summary="This is a student and group management app🚀",
    version="0.0.1",
    contact={
        "name": "ZhangJiyao",
    },
openapi_tags=tags_metadata

)

#@asynccontextmanager
#async def lifespan(app: FastAPI):
create_db_and_tables()

app.include_router(router)

#if __name__ == "__main__":
#    uvicorn.run(app)



