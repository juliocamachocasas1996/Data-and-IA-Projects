"""
Test script to verify pandas installation and basic functionality
"""

import pandas as pd

print("Pandas version:", pd.__version__)

# Create a simple DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Paris', 'London']
}

df = pd.DataFrame(data)

print("\nDataFrame created successfully:")
print(df)

print("\nDataFrame info:")
print(df.info())

print("\nDataFrame statistics:")
print(df.describe())

print("\n✓ Pandas is working correctly!")
