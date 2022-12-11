# .\app.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
def get_root():
    """Returns a dictionary of 'Hello': 'World'"""
    return {"Hello": "World"}


@app.get("/test")
def get_test():
    """Returns a dictionary of 'hell': 'yeah'"""
    return {"hell": "yeah"}

lambda_handler = Mangum(app, lifespan="off")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", port=5000, log_level="info", reload=True)