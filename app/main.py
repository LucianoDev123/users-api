from fastapi import FastAPI

app = FastAPI(title="Users API")


@app.get("/")
def root():
    return {"message": "Users API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}