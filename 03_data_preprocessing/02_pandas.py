import pandas as pd
data=[1,2,3,4,5]
# create a Series
series=pd.Series(data,index=["a","b","c","d","e"])
print(series)
# Accessing element by index label
print(series["c"]) 


#  DataFrame (2D Data)
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [25, 30, 25, 30, 35],
    "Salary": [50000, 60000, 52000, 58000, 70000]
}


df=pd.DataFrame(data)
print(df)
# save DataFrame to CSV file
df.to_csv("output.csv", index=False)
# save DataFrame to Excel file
df.to_excel("output.xlsx", index=False)
# save DataFrame to JSON file
df.to_json("output.json", orient="records", lines=True)


# read DataFrame from CSV file
df_from_csv=pd.read_csv("output.csv")
print(df_from_csv)
# read DataFrame from Excel file
df_from_excel=pd.read_excel("output.xlsx")
print(df_from_excel)
# read DataFrame from JSON file
df_from_json=pd.read_json("output.json", orient="records", lines=True)
print(df_from_json) 


# dataframe operations
print(df.head())  # Display first few rows
print(df.tail())  # Display last few rows
print(df.describe())  # Summary statistics


# selecting columns
print(df["Name"])  # Select a single column
#selecting row
print(df.loc[0])  # Select a row by index label
print(df.iloc[1])  # Select a row by index position


# removing columns
df.drop(columns=["Salary"], inplace=True)  # Remove a column
print(df)

#removing rows
df.loc[3] = ["David", 40, 80000]  # Add new row
print(df)
df.drop(3, axis=0, inplace=True)  # Remove row


# Grouping Data
print(df.groupby("Age")[["Salary"]].mean())
