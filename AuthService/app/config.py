import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost/User")
SECRET_KEY = "926e3c3b282f22e6c09ed7f3824deedc37993d40e6f90c08c2bc07cbf710fca6"
