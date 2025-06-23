from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Welcome to the Notes Manager API"}

@app.get("/about")
def about():
    return {
        "name": "Notes Manager API",
        "version": "1.0.0",
        "description": "An API for managing notes with features like creating, updating, and deleting notes.",
        "author": "Md Somrat Sheikh"
    }