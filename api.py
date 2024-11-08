from fastapi import FastAPI, HTTPException
from database_manager import ApiDatabaseManager

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
