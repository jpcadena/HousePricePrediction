"""This is the main file to run the fastapi server.
"""
import json
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from functions import predict_input
# from house_price_prediction import house_price_prediction_model

with open('config.json', 'r', encoding="utf8") as f:
    config = json.load(f)
PORT = config['PORT']
HOSTNAME = config['HOSTNAME']
INPUT_FILENAME = config['INPUT_FILENAME']
OUTPUT_FILENAME = config['OUTPUT_FILENAME']

app = FastAPI()
with open(OUTPUT_FILENAME, "rb") as file:
    house_price_model = pickle.load(file)
# house_price_model = house_price_prediction_model()


class HousePricePredIn(BaseModel):
    """This is the class for House Price prediction input data."""
    # def __init__(self):
    #     """This is the init method for the class and its parameters."""
    BsmtFinSF1: float
    GarageYrBlt: int
    FrstFlrSF: float
    GarageArea: float
    TotalBsmtSF: float
    YearBuilt: int
    GarageCars: int
    GrLivArea: float
    OverallQual: int


class HousePricePredOut(BaseModel):
    """This is the class for the House Price predicted output data."""
    sale_price: float


@app.get('/')
async def index():
    """Async method that shows a message at index html page."""
    return {'msg': 'Hello from House Price Prediction API'}


@app.post('/house-price-predictions', response_model=HousePricePredOut)
async def predict_house_price(house_price_pred_in: HousePricePredIn):
    """POST function with RESTful API to return the predicted value."""
    print('Nuevo request para predecir el precio de una casa:',
          house_price_pred_in)
    input_values = [house_price_pred_in.BsmtFinSF1,
                    house_price_pred_in.GarageYrBlt,
                    house_price_pred_in.FrstFlrSF,
                    house_price_pred_in.GarageArea,
                    house_price_pred_in.TotalBsmtSF,
                    house_price_pred_in.YearBuilt,
                    house_price_pred_in.GarageCars,
                    house_price_pred_in.GrLivArea,
                    house_price_pred_in.OverallQual]
    numeric_cols = ['BsmtFinSF1', 'GarageYrBlt', '1stFlrSF', 'GarageArea',
                    'TotalBsmtSF', 'YearBuilt', 'GarageCars', 'GrLivArea',
                    'OverallQual']
    data_input = {numeric_cols[i]: input_values[i] for i in
                  range(len(numeric_cols))}
    predicted_price = round(predict_input(house_price_model, data_input,
                                          numeric_cols), 2)
    return HousePricePredOut(sale_price=predicted_price)


if __name__ == '__main__':
    uvicorn.run(app, host=HOSTNAME, port=PORT, debug=True)
