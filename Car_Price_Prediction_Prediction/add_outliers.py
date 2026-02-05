import json

notebook_path = 'car_price_full_pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = []
for cell in nb['cells']:
    new_cells.append(cell)
    
    # Insert Outlier Handling in Section 3, after missing value treatment
    if cell['cell_type'] == 'code' and "df = df.dropna()" in "".join(cell['source']):
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 3.1 Outlier Management\n",
                "Outliers can disproportionately influence the coefficients of a Linear Regression model. We use the Interquartile Range (IQR) method to detect extreme values in the target variable (`Price`) and primary numerical features."
            ]
        })
        new_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Visualizing outliers using Box Plots\n",
                "plt.figure(figsize=(12, 5))\n",
                "plt.subplot(1, 2, 1)\n",
                "sns.boxplot(y=df['Price'], color='skyblue')\n",
                "plt.title('Price Distribution & Potential Outliers')\n",
                "\n",
                "plt.subplot(1, 2, 2)\n",
                "sns.boxplot(y=df['Mileage'], color='salmon')\n",
                "plt.title('Mileage Distribution & Potential Outliers')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "# Handling Outliers (Example: Capping or Removal)\n",
                "# For this dataset, values are within realistic market ranges, \n",
                "# but we validate they don't exceed +/- 3 Standard Deviations for stability.\n",
                "initial_count = len(df)\n",
                "for col in ['Price', 'Mileage']:\n",
                "    upper_limit = df[col].mean() + 3 * df[col].std()\n",
                "    lower_limit = df[col].mean() - 3 * df[col].std()\n",
                "    df = df[(df[col] <= upper_limit) & (df[col] >= lower_limit)]\n",
                "\n",
                "print(f\"Rows removed during outlier cleaning: {initial_count - len(df)}\")"
            ]
        })

nb['cells'] = new_cells
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Outlier Management section added successfully.")
