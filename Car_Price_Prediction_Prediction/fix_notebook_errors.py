import json

notebook_path = 'car_price_full_pipeline.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = []
for cell in nb['cells']:
    # Sanitization: Fix previous failed renaming attempts
    for i, line in enumerate(cell['source']):
        if "raw_raw_df" in line:
            cell['source'][i] = line.replace("raw_raw_df", "raw_df")
    
    # Fix Section 2.1: Descriptive Statistics to use raw_df instead of df
    # if it's before Section 3 which defines df.
    if cell['cell_type'] == 'code' and "df.describe().round(2)" in "".join(cell['source']) and "raw_df.describe()" not in "".join(cell['source']):
        source = "".join(cell['source'])
        source = source.replace("df.describe()", "raw_df.describe()")
        cell['source'] = [source]
    
    # Fix select_dtypes to remove 'str' which causes TypeError in some Pandas versions
    if cell['cell_type'] == 'code' and "select_dtypes(include=['object', 'str'])" in "".join(cell['source']):
        source = "".join(cell['source'])
        source = source.replace("select_dtypes(include=['object', 'str'])", "select_dtypes(include=['object'])")
        cell['source'] = [source]
    
    # Section 6: Model Parameter Interpretation fix for variable name
    if cell['cell_type'] == 'code' and "model = pipeline.named_steps['regressor']" in "".join(cell['source']):
        source = "".join(cell['source'])
        source = source.replace("pipeline.named_steps", "model_pipeline.named_steps")
        cell['source'] = [source]

    new_cells.append(cell)

nb['cells'] = new_cells

# Fix metadata kernel
nb['metadata']['kernelspec'] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook variable usage and select_dtypes fixed.")
