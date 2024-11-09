from fastapi import FastAPI, HTTPException
from crypto import Crypto
from database_manager import ApiDatabaseManager
from pydantic import BaseModel, Field, HttpUrl


class CreatePassword(BaseModel):
    site: HttpUrl = Field(..., description="The website name")
    password: str = Field(..., description="The password")


app = FastAPI()
db = ApiDatabaseManager()


@app.get("/api/v1/passwords/{api_key}")
async def get_passwords(api_key: str):
    try:
        return db.get_user_passwords_api(api_key)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing database: {str(e)}"
        )


@app.get("/api/v1/username/{api_key}")
async def get_user(api_key: str):
    try:
        user_name = db.get_user_by_api_key(api_key)
        if user_name:
            return {"username": user_name}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing database: {str(e)}"
        )


@app.post("/api/v1/passwords/add/{api_key}")
async def add_password(api_key: str, password_data: CreatePassword) -> dict:
    try:
        user_name = db.get_user_by_api_key(api_key)
        user_password = db.get_password_by_name(user_name)
        if user_name:
            db.save_password(
                user_name,
                str(password_data.site),
                Crypto.encrypt(password_data.password, user_password),
            )
            return {"message": "Password added successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error accessing database: {str(e)}"
        )
