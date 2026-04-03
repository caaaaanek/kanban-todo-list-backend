from fastapi import FastAPI

app = FastAPI(title="Kanban Todo List API")


@app.get("/")
def root():
    return {"message": "Kanban Todo List API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
