import csv
import requests
import sys
import urllib.parse
import yfinance as yf

def main():
    
    telegram_apikey = sys.argv[1]
    chat_id         = sys.argv[2]

    # Read stock RS file
    with open('output/rs_stocks.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)

    # Filter the rows where the first three columns are all > 80
    filtered_data = [row for row in data if all(float(col) > 80 for col in row[6:9])]

    result_list = []
    industry_sector_dict = {}
    for row in filtered_data:
        result_list.append(row[1])
        try:
            industry_sector_dict[f"{row[3]}-{row[2]}"]
            industry_sector_dict[f"{row[3]}-{row[2]}"] += 1
        except KeyError:
            industry_sector_dict[f"{row[3]}-{row[2]}"] = 1            
           
    result_list.sort()
    print(result_list)
    sorted_industry_sector_dict = sorted(industry_sector_dict.items(), key=lambda x: x[1], reverse=True)
    print(dict(sorted_industry_sector_dict))
    
    filtered_by_over_10b_list = []
    for x in result_list:
        try:
            stock = yf.Ticker(x)
            # Get the market capitalization
            market_cap = stock.info.get('marketCap', 0)
            # Check if the market cap is over 1 billion (10^10)
            if market_cap > 1000000000:
                filtered_by_over_10b_list.append(x)
        except:
            pass
    print(filtered_by_over_10b_list)
    
    results = ','.join(result_list)
    message = "Stocks RS rating > 80 in past months\n\n"
    message += results
    message += "\n\n"
    message += str(sorted_industry_sector_dict)
        
    
    # message += f"\n\nFiltered over 10 billion:\n\n"
    # stock_list2 = ', '.join(filtered_by_over_10b_list)
    # # message += stock_list2
    # message += "\n\n"
    # # message2 = str(sorted_industry_sector_dict)
    
    message = urllib.parse.quote(message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url)

    
    # read Industries RS file
    with open('output/rs_industries.csv', 'r') as file2:
        reader2 = csv.reader(file2)
        next(reader2)
        data2 = list(reader2)

    ### Filter the rows where the first three columns are all > 80
    industry_filtered_data = [row for row in data2 if all(float(col) >= 90 for col in row[4:7])] # Percentile, 1-month and 3-month top

    industry_result_list = []
    for row in industry_filtered_data:
        industry_result_list.append(f"{row[1]}-{row[2]} {row[4:7]} {row[8]}") # Sample 1,Copper,Basic Materials,119.33,99,99,97,46,"HBM,TGB,SCCO,ERO,FCX"
           
    
    print(industry_result_list)
    
    industry_results = '\n\n'.join(industry_result_list)
    industry_message = "Industry RS rating > 80\n\n"
    industry_message += industry_results

    industry_message = urllib.parse.quote(industry_message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={industry_message}"
    requests.get(url)


if __name__ == "__main__":
    main()
