import csv
import requests
import sys
import urllib.parse

def main():
    
    telegram_apikey = sys.argv[1]
    chat_id         = sys.argv[2]

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-token', type=str)
    # parser.add_argument('-chatid', type=str)
    # args = parser.parse_args()
    
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
        result_list.append(row[1])
           
    result_list.sort()
    print(result_list)
    
    results = ','.join(result_list)
    message = "Stocks with RS rating > 80\n\n"
    message += results

    message = urllib.parse.quote(message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"

    requests.get(url)

    # read rs_industries
    with open('output/rs_industries.csv', 'r') as file2:
        reader2 = csv.reader(file2)
        next(reader2)
        data2 = list(reader2)

    # Filter the rows where the first three columns are all > 80
    industry_filtered_data = [row for row in data2 if all(float(col) >= 90 for col in row[4:7])] #1-month and 3-month top

    # Print the filtered rows
    industry_result_list = []
    for row in industry_filtered_data:
        industry_result_list.append(f"{row[1]}-{row[2]} {row[4:7]}")
           
    
    print(industry_result_list)
    
    industry_results = ','.join(industry_result_list)
    industry_message = "Stocks with Industry RS rating > 80\n\n"
    industry_message += industry_results

    industry_message = urllib.parse.quote(industry_message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={industry_message}"

    requests.get(url)


if __name__ == "__main__":
    main()
