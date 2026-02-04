import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots if it doesn't exist
os.makedirs('plots', exist_ok=True)

# Load data
df = pd.read_csv('car_price_prediction_.csv')

# Basic Info
print("--- Dataset Info ---")
print(df.info())

print("\n--- Summary Statistics ---")
print(df.describe(include='all'))

# Missing Values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Cleaning
# Drop Car ID - irrelevant for prediction
if 'Car ID' in df.columns:
    df.drop('Car ID', axis=1, inplace=True)

# Exploratory Visualizations
plt.figure(figsize=(10, 6))
sns.histplot(df['Price'], kde=True)
plt.title('Price Distribution')
plt.savefig('plots/price_dist.png')
plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(x='Brand', y='Price', data=df)
plt.title('Price by Brand')
plt.xticks(rotation=45)
plt.savefig('plots/price_by_brand.png')
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Year', y='Price', data=df)
plt.title('Price vs Year')
plt.savefig('plots/price_vs_year.png')
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Mileage', y='Price', data=df)
plt.title('Price vs Mileage')
plt.savefig('plots/price_vs_mileage.png')
plt.close()

# Correlation Matrix for numeric features
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('plots/correlation_matrix.png')
plt.close()

# Save cleaned data
df.to_csv('cleaned_car_price_data.csv', index=False)
print("\nCleaned data saved to 'cleaned_car_price_data.csv'")
