# app/main.py
from fastapi import FastAPI
from app.game import simulate_battle

app = FastAPI(title="Game CI/CD Demo")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/simulate")
def simulate():
    return simulate_battle()
