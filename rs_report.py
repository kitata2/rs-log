import csv
import requests
import sys

def main():
    telegram_apikey = sys.argv[0]
    chat_id         = sys.argv[1]
    
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
           
    message = "Stocks with RS rating > 80\n\n"
    message += ','.join(result_list)

    message = urllib.parse.quote(message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)


if __name__ == "__main__":
    main()
