from fastapi import FastAPI

app = FastAPI()
@app.get("/")

def root():
    return {"message": "Leetcode Tracker API is running"}