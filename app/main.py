# app/main.py
from fastapi import FastAPI
from app.routes import collateral

app = FastAPI()

# Include routes
app.include_router(collateral.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Collateral Switching API"}
