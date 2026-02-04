import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

def train_and_save_model(data_path, model_output, preprocessor_output):
    # Load cleaned data
    df = pd.read_csv(data_path)
    
    # Define features and target
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
    
    # Create the full pipeline with model
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared Score: {r2}")
    
    # Save the entire pipeline (including preprocessor and model)
    with open(model_output, 'wb') as f:
        pickle.dump(model_pipeline, f)
    
    print(f"Model pipeline saved to {model_output}")
    
    # Also save metadata for EDA endpoints
    metadata = {
        'categorical_cols': categorical_cols,
        'numerical_cols': numerical_cols,
        'brands': df['Brand'].unique().tolist(),
        'fuel_types': df['Fuel Type'].unique().tolist(),
        'transmissions': df['Transmission'].unique().tolist(),
        'conditions': df['Condition'].unique().tolist(),
        'models': df['Model'].unique().tolist(),
        'mse': mse,
        'r2': r2
    }
    with open('metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)
    print("Metadata saved to metadata.pkl")

if __name__ == "__main__":
    train_and_save_model('cleaned_car_price_data_logical.csv', 'model_pipeline.pkl', 'preprocessor.pkl')
