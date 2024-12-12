# 使用 Python 基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
#COPY ./.env.example /app/

#ENV SQLITE_DATABASE=/app/database.db
#RUN mkdir -p /data && touch /data/database.db


# 暴露 FastAPI 应用程序端口
EXPOSE 8000

# 启动 FastAPI 应用程序
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

