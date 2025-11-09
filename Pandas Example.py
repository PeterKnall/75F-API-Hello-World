
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
# Example Date Stamp: # 2025-11-08T14:39:00-05:00 Detroit

# Matches optional sign, digits before decimal, optional decimal and digits after, or just a decimal and digits.
# Also handles scientific notation (e.g., 1.23e-04)
"""

ids = "@52bdc021-71d3-4479-903e-0b0986a993ee,@52b2309a-10ec-4578-af76-8c1130c58044"

float_pattern = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'

pd.set_option('display.max_columns', None)                  # Pandas option to display all columns (do not use "...")
these_rows = results["rows"][0]["data"]                     # Navigate thorough the dict and find the Trend Data List
df = pd.DataFrame(these_rows)                               # Store that list in a Pandas Data Frame

# Wrangle the data value
df['str_value'] = df['val'].str.extract(float_pattern)[0]   # Extract the "number" portion of the value columns
df['value'] = pd.to_numeric(df['str_value'])                # Convert the text "number" portion to a numeric type

# Wrangle the date stamp
df['date_value1'] = df['ts'].str.split(":", n=1).str[1]     # Remove the "n:" portion of the date stamp
df['date_value2'] = df['date_value1'].str.split(" ", n=1).str[0]  # Remove the city portion of the date stamp (Detroit)
df['time'] = pd.to_datetime(df['date_value2'], format="ISO8601")  # Convert to datetime object

# Remove unneeded columns / clean-up df
df = df.drop("val", axis=1)
df = df.drop("str_value", axis = 1)
df = df.drop("ts", axis=1)
df = df.drop("date_value1", axis=1)
df = df.drop("date_value2", axis=1)

# print(df)

df.plot(x='time', y='value')
plt.show()
"""