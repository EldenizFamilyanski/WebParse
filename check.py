import pandas as pd

#
# example_columns = pd.read_csv("import_example.csv", sep=";").columns
# print(example_columns)


# df_correct_columns = pd.DataFrame(df, columns=example_columns)

# print(df_correct_columns.columns)
# del df_correct_columns["Column 1"]
# df_correct_columns.to_csv("correct_columns.csv")
df = pd.read_csv("data2.csv")
df_correct_columns = pd.DataFrame()
for index, row in df.iterrows():
    df.loc[index, "SKU"] = str(int(float(df.loc[index, "SKU"])))


df_correct_columns["SKU"] = df["SKU"]
df_correct_columns["Category"] = df["Category"]
df_correct_columns["Title"] = df["Title"]
df_correct_columns["Description"] = df["Description"]
df_correct_columns["Text"] = df["Text"]
df_correct_columns["Photo"] = df["Photo"]
df_correct_columns["Price"] = df["Price"]
df_correct_columns["Quantity"] = df["Quantity"]
df_correct_columns["Price Old"] = df["Price Old"]
df_correct_columns["Editions"] = df["Editions"]
df_correct_columns["Modifications"] = df["Modifications"]
df_correct_columns["External ID"] = df["External ID"]
df_correct_columns["Parent UID"] = df["Parent UID"]

df_correct_columns.to_csv("correct_columns.csv", index=False)
df_ready_slice = df_correct_columns.iloc[0:50]
df_ready_slice.to_csv("ready_slice.csv", index=False)
