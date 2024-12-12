import uvicorn
from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth,updata,refresh,history,logout

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Included Routes
app.include_router(auth.router)
app.include_router(updata.router)
app.include_router(refresh.router)
app.include_router(history.router)
app.include_router(logout.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)