from fastapi import FastAPI
import pandas as pd

# Create FastAPI application
app = FastAPI(
    title="Skin Clinic Campaign Analysis API",
    description="Customer campaign response analysis",
    version="1.0"
)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv("skin_clinic_campaign.csv")

# Convert campaign response from Yes/No to 1/0
# Yes = 1
# No = 0

df["Response_Flag"] = (
    df["Response_to_Campaign"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("yes")
    .astype(int)
)


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Skin Clinic Campaign Analysis API",
        "endpoint": "/campaign-analysis"
    }


# --------------------------------------------------
# Campaign Analysis endpoint
# --------------------------------------------------

@app.get("/campaign-analysis")
def campaign_analysis():

    # ==================================================
    # 1. Gender vs Campaign Response
    # ==================================================

    gender = (
        df.groupby("Gender")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=("Response_Flag", "sum"),
            Response_Rate=("Response_Flag", "mean")
        )
        .reset_index()
    )

    # Convert response rate to percentage
    gender["Response_Rate"] = (
        gender["Response_Rate"] * 100
    ).round(2)


    # ==================================================
    # 2. Age Group vs Campaign Response
    # ==================================================

    age = (
        df.groupby("AgeGroup")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=("Response_Flag", "sum"),
            Response_Rate=("Response_Flag", "mean")
        )
        .reset_index()
    )

    # Convert response rate to percentage
    age["Response_Rate"] = (
        age["Response_Rate"] * 100
    ).round(2)


    # ==================================================
    # 3. Purchase Last Quarter vs Campaign Response
    # ==================================================

    purchase = (
        df.groupby("Purchase_Last_Quarter")
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=("Response_Flag", "sum"),
            Response_Rate=("Response_Flag", "mean")
        )
        .reset_index()
    )

    # Convert response rate to percentage
    purchase["Response_Rate"] = (
        purchase["Response_Rate"] * 100
    ).round(2)


    # ==================================================
    # 4. Product Usage vs Campaign Response
    # ==================================================

    # Create a copy of the dataframe
    temp_df = df.copy()

    # Categorize customers based on unique products purchased
    temp_df["Product_Usage"] = pd.cut(
        temp_df["Unique_Products_Purchased"],
        bins=[0, 4, 8, float("inf")],
        labels=["1-4", "5-8", ">8"]
    )

    product = (
        temp_df.groupby(
            "Product_Usage",
            observed=False
        )
        .agg(
            Total_Customers=("CustID", "count"),
            Responded=("Response_Flag", "sum"),
            Response_Rate=("Response_Flag", "mean")
        )
        .reset_index()
    )

    # Convert response rate to percentage
    product["Response_Rate"] = (
        product["Response_Rate"] * 100
    ).round(2)


    # ==================================================
    # Return all analysis tables
    # ==================================================

    return {
        "gender_analysis":
            gender.to_dict(orient="records"),

        "age_analysis":
            age.to_dict(orient="records"),

        "purchase_analysis":
            purchase.to_dict(orient="records"),

        "product_usage_analysis":
            product.to_dict(orient="records")
    }
