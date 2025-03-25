Here’s a quick Pandas DataFrame (df) cheatsheet to help you efficiently navigate, manipulate, and analyze data:

---

### **1. Loading Data**
```python
import pandas as pd

# Load a CSV into a DataFrame
df = pd.read_csv("file.csv")

# Save DataFrame to a new CSV file
df.to_csv("output.csv", index=False)
```

---

### **2. Exploring the Data**
```python
# View first/last 5 rows
print(df.head())
print(df.tail())

# Summary of the DataFrame
print(df.info())

# Summary statistics for numerical columns
print(df.describe())

# Check the shape (rows, columns)
print(df.shape)

# Check column names
print(df.columns)

# Check data types of each column
print(df.dtypes)
```

---

### **3. Accessing Columns and Rows**
```python
# Access a single column
print(df["ColumnName"])

# Access multiple columns
print(df[["Column1", "Column2"]])

# Access rows by index
print(df.iloc[0])    # First row (index starts at 0)
print(df.iloc[5])    # Sixth row

# Access rows by label (if your index is meaningful)
print(df.loc[0])     # First row (default numerical index)
```

---

### **4. Filtering and Subsetting**
```python
# Filter rows based on a condition
filtered_df = df[df["ColumnName"] > 10]

# Multiple conditions (use `&` for AND, `|` for OR)
filtered_df = df[(df["Column1"] > 10) & (df["Column2"] == "Value")]

# Select specific rows and columns
subset = df.loc[0:5, ["Column1", "Column2"]]  # First 6 rows, specific columns
```

---

### **5. Adding/Modifying Columns**
```python
# Add a new column
df["NewColumn"] = df["ExistingColumn"] * 2

# Modify an existing column
df["ExistingColumn"] = df["ExistingColumn"] / 100
```

---

### **6. Removing Data**
```python
# Drop a column
df = df.drop(columns=["ColumnName"])

# Drop rows by index
df = df.drop(index=[0, 1])  # Remove first and second rows

# Remove duplicates
df = df.drop_duplicates()
```

---

### **7. Sorting**
```python
# Sort rows by a column
df = df.sort_values("ColumnName", ascending=True)

# Sort by multiple columns
df = df.sort_values(["Column1", "Column2"], ascending=[True, False])
```

---

### **8. Grouping and Aggregating**
```python
# Group by a column and calculate the mean
grouped = df.groupby("ColumnName").mean()

# Aggregate multiple functions
aggregated = df.groupby("ColumnName").agg({"Column1": "sum", "Column2": "mean"})
```

---

### **9. Handling Missing Data**
```python
# Check for missing values
print(df.isnull().sum())

# Drop rows/columns with missing data
df = df.dropna()         # Drop rows with missing values
df = df.dropna(axis=1)   # Drop columns with missing values

# Fill missing values
df["ColumnName"] = df["ColumnName"].fillna(0)  # Fill with 0
df["ColumnName"] = df["ColumnName"].fillna(df["ColumnName"].mean())  # Fill with mean
```

---

### **10. Merging and Joining**
```python
# Merge two DataFrames
merged_df = pd.merge(df1, df2, on="KeyColumn")

# Concatenate DataFrames (stacking)
concatenated_df = pd.concat([df1, df2], axis=0)  # Vertical stack (rows)
concatenated_df = pd.concat([df1, df2], axis=1)  # Horizontal stack (columns)
```

---

### **11. Export to Other Formats**
```python
# Save to Excel
df.to_excel("file.xlsx", index=False)

# Save to JSON
df.to_json("file.json")
```

---

This should cover the basics as well as some intermediate operations in Pandas! Let me know if you want examples of any specific functionality. 🚀