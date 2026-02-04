from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import pickle
import os
import base64
from typing import List, Dict

app = FastAPI(title="Car Price Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and metadata
try:
    with open('model_pipeline.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    df_cleaned = pd.read_csv('cleaned_car_price_data_logical.csv')
except Exception as e:
    print(f"Error loading model or data: {e}")
    model = None
    metadata = {}
    df_cleaned = None

class CarFeatures(BaseModel):
    Brand: str
    Year: int
    Engine_Size: float
    Fuel_Type: str
    Transmission: str
    Mileage: float
    Condition: str
    Model: str

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/eda/metadata")
def get_metadata():
    return metadata

@app.get("/eda/stats")
def get_stats():
    if df_cleaned is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    # Return some basic statistics
    stats = {
        "total_rows": len(df_cleaned),
        "columns": df_cleaned.columns.tolist(),
        "brand_counts": df_cleaned['Brand'].value_counts().to_dict(),
        "fuel_type_counts": df_cleaned['Fuel Type'].value_counts().to_dict(),
        "avg_price_by_brand": df_cleaned.groupby('Brand')['Price'].mean().to_dict(),
        "top_models": df_cleaned['Model'].value_counts().head(10).to_dict()
    }
    return stats

@app.get("/eda/sample")
def get_sample(n: int = 10):
    if df_cleaned is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    return df_cleaned.head(n).to_dict(orient='records')

@app.get("/eda/plots/{plot_name}")
def get_plot(plot_name: str):
    plot_path = f"plots/{plot_name}.png"
    if not os.path.exists(plot_path):
        raise HTTPException(status_code=404, detail="Plot not found")
    
    with open(plot_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return {"image": encoded_string}

@app.get("/download-report")
def download_report():
    report_path = "final_report.pdf"
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(report_path, media_type='application/pdf', filename="Car_Price_Report.pdf")

@app.post("/predict")
def predict(features: CarFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Convert pydantic model to dataframe with correct column names (matching the training data)
    input_data = pd.DataFrame([{
        'Brand': features.Brand,
        'Year': features.Year,
        'Engine Size': features.Engine_Size,
        'Fuel Type': features.Fuel_Type,
        'Transmission': features.Transmission,
        'Mileage': features.Mileage,
        'Condition': features.Condition,
        'Model': features.Model
    }])
    
    try:
        prediction = model.predict(input_data)[0]
        return {"predicted_price": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
