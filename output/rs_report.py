import csv

# Read the CSV file
with open('rs_stocks.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Filter the rows where the first three columns are all > 80
filtered_data = [row for row in data if all(float(col) > 80 for col in row[6:9])]

# Print the filtered rows
for row in filtered_data:
    row[