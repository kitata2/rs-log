import csv

# Read the CSV file
with open('output/rs_stocks.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    data = list(reader)

# Filter the rows where the first three columns are all > 80
filtered_data = [row for row in data if all(float(col) > 80 for col in row[6:9])]

# Print the filtered rows
result_list = []
for row in filtered_data:
    print(row)
    result_list.append(row[1])
    
