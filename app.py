from fastapi import FastAPI, Request
from typing import Optional
from uvicorn import run as app_run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bank_churn.components.model_predictor import CostPredictor, BankChurnData
from bank_churn.constants import APP_HOST, APP_PORT
from bank_churn.pipeline.training_pipeline import TrainingPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.LIMIT_BAL: Optional[str] = None
        self.SEX: Optional[str] = None
        self.EDUCATION: Optional[str] = None
        self.MARRIAGE: Optional[str] = None
        self.AGE: Optional[str] = None
        self.PAY_0: Optional[str] = None
        self.PAY_1: Optional[str] = None
        self.PAY_2: Optional[str] = None
        self.PAY_3: Optional[str] = None
        self.PAY_4: Optional[str] = None
        self.PAY_5: Optional[str] = None
        self.BILL_AMT1: Optional[str] = None
        self.BILL_AMT2: Optional[str] = None
        self.BILL_AMT3: Optional[str] = None
        self.BILL_AMT4: Optional[str] = None
        self.BILL_AMT5: Optional[str] = None
        self.BILL_AMT6: Optional[str] = None
        self.PAY_AMT1: Optional[str] = None
        self.PAY_AMT2: Optional[str] = None
        self.PAY_AMT3: Optional[str] = None
        self.PAY_AMT4: Optional[str] = None
        self.PAY_AMT5: Optional[str] = None
        self.PAY_AMT6: Optional[str] = None
    async def get_bankchurn_data(self):
        form = await self.request.form()
        self.LIMIT_BAL = form.get("LIMIT_BAL")
        self.SEX = form.get("SEX")
        self.EDUCATION = form.get("EDUCATION")
        self.MARRIAGE = form.get("MARRIAGE")
        self.AGE = form.get("AGE")
        self.PAY_0 = form.get("PAY_0")
        self.PAY_1= form.get("PAY_1")
        self.PAY_2 = form.get("PAY_2")
        self.PAY_3 = form.get("PAY_3")
        self.PAY_4 = form.get("PAY_4")
        self.PAY_5 = form.get("PAY_5")
        self.BILL_AMT1 = form.get("BILL_AMT1")
        self.BILL_AMT2 = form.get("BILL_AMT2")
        self.BILL_AMT3 = form.get("BILL_AMT3")
        self.BILL_AMT4 = form.get("BILL_AMT4")
        self.BILL_AMT5 = form.get("BILL_AMT5")
        self.BILL_AMT6 = form.get("BILL_AMT6")
        self.PAY_AMT1 = form.get("PAY_AMT1")
        self.PAY_AMT2 = form.get("PAY_AMT2")
        self.PAY_AMT3 = form.get("PAY_AMT3")
        self.PAY_AMT4 = form.get("PAY_AMT4")
        self.PAY_AMT5 = form.get("PAY_AMT5")
        self.PAY_AMT6 = form.get("PAY_AMT6")


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainingPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.get("/predict")
async def predictGetRouteClient(request: Request):
    try:

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": "Rendering"},
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/predict")
async def predictRouteClient(request: Request):
    try:

        form = DataForm(request)
        await form.get_bankchurn_data()

        bankchurn_data = BankChurnData(
            LIMIT_BAL=form.LIMIT_BAL,
            SEX=form.SEX,
            EDUCATION=form.EDUCATION,
            MARRIAGE=form.MARRIAGE,
            AGE=form.AGE,
            PAY_0=form.PAY_0,
            PAY_1=form.PAY_1,
            PAY_2=form.PAY_2,
            PAY_3=form.PAY_3,
            PAY_4=form.PAY_4,
            PAY_5=form.PAY_5,
            BILL_AMT1=form.BILL_AMT1,
            BILL_AMT2=form.BILL_AMT2,
            BILL_AMT3=form.BILL_AMT3,
            BILL_AMT4=form.BILL_AMT4,
            BILL_AMT5=form.BILL_AMT5,
            BILL_AMT6=form.BILL_AMT6,
            PAY_AMT1=form.PAY_AMT1,
            PAY_AMT2=form.PAY_AMT2,
            PAY_AMT3=form.PAY_AMT3,
            PAY_AMT4=form.PAY_AMT4,
            PAY_AMT5=form.PAY_AMT5,
            PAY_AMT6=form.PAY_AMT6
        )

        cost_df = bankchurn_data.get_input_data_frame()
        cost_predictor = CostPredictor()
        cost_value = round(cost_predictor.predict(X=cost_df)[0], 2)
        if cost_value == "1":
            answer = "not_churn"
        else:
            answer = "churn"

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "context": answer},
        )


    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)



# try:
#     train_pipeline = TrainingPipeline()
#     train_pipeline.run_pipeline()
#
# except Exception as e:
#         raise e