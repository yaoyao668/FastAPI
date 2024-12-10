import uvicorn
from fastapi import FastAPI
from app.database import engine
from app import models , auth

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 包含路由
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)