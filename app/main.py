from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.calculator import CalculatorError, calculate_expression
from app.database import (
    add_history,
    delete_history,
    get_history,
    init_database,
)


app = FastAPI(title="Calculator Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculateRequest(BaseModel):
    expression: str


@app.on_event("startup")
def startup():
    init_database()


@app.get("/")
def root():
    return {"message": "Calculator Backend is running"}


@app.post("/api/calculate")
def calculate(request: CalculateRequest):
    try:
        result = calculate_expression(request.expression)

        history_id = add_history(
            request.expression,
            result,
        )

        return {
            "id": history_id,
            "expression": request.expression,
            "result": result,
        }

    except CalculatorError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
@app.get("/api/history")
def history():
    return {
        "history": get_history(),
    }
@app.delete("/api/history/{history_id}")
def delete_history_record(history_id: int):
    deleted = delete_history(history_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="History record not found.",
        )

    return {
        "message": "History record deleted successfully.",
        "id": history_id,
    }