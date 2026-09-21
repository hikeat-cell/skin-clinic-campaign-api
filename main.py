
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI(
    title="Skin Clinic Campaign Analysis",
    description="Analysis of customer response to a skin clinic marketing campaign"
)

# Load dataset
df = pd.read_csv("skin_clinic_campaign.csv")


@app.get("/")
def home():
    return {
        "message": "Skin Clinic Campaign Analysis API",
        "endpoint": "/campaign-analysis"
    }


@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():

    # ----------------------------------------
    # 1. Gender vs Campaign Response
    # ----------------------------------------

    gender_response = (
        df.groupby("Gender")["Response_to_Campaign"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    gender_response.columns = [
        "Gender",
        "Response Rate (%)"
    ]


    # ----------------------------------------
    # 2. Age Group vs Campaign Response
    # ----------------------------------------

    age_response = (
        df.groupby("AgeGroup")["Response_to_Campaign"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    age_response.columns = [
        "Age Group",
        "Response Rate (%)"
    ]


    # ----------------------------------------
    # 3. Purchase Last Quarter vs Response
    # ----------------------------------------

    purchase_response = (
        df.groupby("purchase_last_quarter_label")[
            "Response_to_Campaign"
        ]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    purchase_response.columns = [
        "Purchase in Last Quarter",
        "Response Rate (%)"
    ]


    # ----------------------------------------
    # 4. Product Usage vs Campaign Response
    # ----------------------------------------

    product_response = (
        df.groupby("product_usage_group")[
            "Response_to_Campaign"
        ]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    product_response.columns = [
        "Product Usage",
        "Response Rate (%)"
    ]


    # Convert tables to HTML

    gender_table = gender_response.to_html(index=False)
    age_table = age_response.to_html(index=False)
    purchase_table = purchase_response.to_html(index=False)
    product_table = product_response.to_html(index=False)


    # ----------------------------------------
    # HTML page
    # ----------------------------------------

    html = f"""
    <html>

    <head>

        <title>Skin Clinic Campaign Analysis</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}

            h1 {{
                text-align: center;
            }}

            h2 {{
                margin-top: 40px;
            }}

            table {{
                border-collapse: collapse;
                width: 600px;
                background-color: white;
            }}

            th, td {{
                border: 1px solid #cccccc;
                padding: 10px;
                text-align: center;
            }}

            th {{
                background-color: #333333;
                color: white;
            }}

        </style>

    </head>


    <body>

        <h1>Skin Clinic Campaign Analysis</h1>


        <h2>1. Gender vs Campaign Response</h2>

        {gender_table}


        <h2>2. Age Group vs Campaign Response</h2>

        {age_table}


        <h2>3. Purchase in Last Quarter vs Campaign Response</h2>

        {purchase_table}


        <h2>4. Product Usage vs Campaign Response</h2>

        {product_table}


    </body>

    </html>
    """

    return HTMLResponse(content=html)
