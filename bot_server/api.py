from fastapi import FastAPI

"""Шина общения и управление ботом"""
app = FastAPI()

@app.post("/")
async def add_new_bot():
    return {"message": "Hello World"}