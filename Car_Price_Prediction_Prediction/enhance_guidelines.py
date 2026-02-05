import json

notebook_path = 'car_price_full_pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = []
for cell in nb['cells']:
    new_cells.append(cell)
    
    # 1. Add Descriptive Statistics after Section 2 Data Loading
    if cell['cell_type'] == 'code' and "raw_df.head()" in "".join(cell['source']):
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### 2.1 Descriptive Statistics\n",
                "To understand the central tendency and dispersion of our numerical features, we perform a descriptive statistical analysis. This helps identify the scale of our data and detect any obvious outliers."
            ]
        })
        new_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Generating descriptive statistics for numerical variables\n",
                "df.describe().round(2)"
            ]
        })

    # 2. Add Enhanced Visual Analysis (Scatter Plot) in Section 4
    if cell['cell_type'] == 'code' and "sns.histplot(df['Price']" in "".join(cell['source']):
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### **Bivariate Analysis: Price vs. Year & Mileage**\n",
                "We examine the relationship between the target variable (`Price`) and its primary numerical predictors to validate market logic (e.g., newer cars should generally cost more)."
            ]
        })
        new_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "\n",
                "# Year vs Price\n",
                "sns.scatterplot(x='Year', y='Price', data=df, ax=ax1, alpha=0.5)\n",
                "ax1.set_title('Price Trend by Manufacturing Year')\n",
                "\n",
                "# Mileage vs Price\n",
                "sns.scatterplot(x='Mileage', y='Price', data=df, ax=ax2, alpha=0.5, color='orange')\n",
                "ax2.set_title('Impact of Mileage on Price')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        })

    # 3. Add Categorical Variable Analysis (Section 5)
    if cell['cell_type'] == 'markdown' and "## 5. Automated Preprocessing Pipeline" in "".join(cell['source']):
        # Insert before Section 5
        # The current 'cell' is the one matching, we need to insert BEFORE it.
        # So we pop it, insert our new cells, then put it back.
        match_cell = new_cells.pop()
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Categorical Variable Analysis\n",
                "Understanding the diversity of categorical features is essential for determining the encoding strategy (e.g., One-Hot Encoding for low-cardinality nominal variables)."
            ]
        })
        new_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Analyzing unique values for categorical features\n",
                "cat_cols = df.select_dtypes(include=['object', 'str']).columns\n",
                "for col in cat_cols:\n",
                "    print(f\"--- {col} Analysis ---\")\n",
                "    print(f\"Unique Count: {df[col].nunique()}\")\n",
                "    print(df[col].value_counts().head(5))\n",
                "    print('\\n') # Fixed escape character"
            ]
        })
        new_cells.append(match_cell)

    # 4. Enhance Model Interpretation in Section 6
    if cell['cell_type'] == 'code' and "r2_score(y_test, y_pred)" in "".join(cell['source']):
         new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### **Model Parameter Interpretation**\n",
                "The Linear Regression model provides interpretable weights for each feature. \n",
                "- **Intercept:** Represents the base price when all numerical features are zero and categorical base levels are selected.\n",
                "- **Coefficients:** Quantify the dollar-value change in Price for every unit increase in predictors like Year or Engine Size."
            ]
        })
         new_cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "model = pipeline.named_steps['regressor']\n",
                "print(f\"Model Intercept: ${model.intercept_:,.2f}\")\n",
                "\n",
                "# Accessing feature names from the pipeline transformer\n",
                "preprocessor = pipeline.named_steps['preprocessor']\n",
                "cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out()\n",
                "num_features = ['Year', 'Engine Size', 'Mileage']\n",
                "all_features = list(num_features) + list(cat_features)\n",
                "\n",
                "coeffs = pd.Series(model.coef_, index=all_features)\n",
                "print('\\nTop Five Positive Predictors:')\n",
                "print(coeffs.sort_values(ascending=False).head(5))"
            ]
        })

nb['cells'] = new_cells
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print("Notebook enhanced successfully with University Requirements.")
