from src.config_reader import load_config
from pathlib import Path
import joblib
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, conint
import os


config_path = "src/config/config.yaml"
config = load_config(config_path)["web"]
model_dir = Path(config["model"]) / config["model_name"]
model = joblib.load(model_dir)

app = FastAPI()


class Req(BaseModel):
    hour: conint(ge=0, le=23)
    day: conint(ge=0)
    row: conint(ge=0, le=7)
    col: conint(ge=0, le=7)


class Res(BaseModel):
    demand: int


@app.post("/predict", response_model=Res)
async def predict(req: Req):
    features = [req.hour, req.row, req.col, req.hour, req.day]
    prediction = model.predict([features])
    return Res(demand=round(prediction[0]))


if __name__ == "__main__":
    uvicorn.run("web.app:app", host=config["host"], port=config["port"], reload=True)
