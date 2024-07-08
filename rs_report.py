import csv
import requests
import sys
import urllib.parse
import yfinance as yf

TWO_BILLION = 2000000000
TEN_BILLION = 10000000000

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

    
    filtered_by_mid_cap_list = []
    filtered_by_over_10b_list = []
    for x in result_list:
        try:
            stock = yf.Ticker(x)
            # Get the market capitalization
            market_cap = stock.info.get('marketCap', 0)
            # Check the market cap
            if (market_cap >= TEN_BILLION): # Large-cap
                filtered_by_over_10b_list.append(x)
            elif (market_cap > TWO_BILLION): # Mid-cap
                    filtered_by_mid_cap_list.append(x)
        except:
            pass   
    
    print(filtered_by_over_10b_list)
    
    sorted_industry_sector_dict = sorted(industry_sector_dict.items(), key=lambda x: x[1], reverse=True) #List of tuples
    print(sorted_industry_sector_dict)
    
    # results = ','.join(result_list)
    # message = "Stocks RS rating > 80 in past months\n\n"
    # message += results
    # message = urllib.parse.quote(message)
    # url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"
    # res = requests.get(url)

    results = ','.join(filtered_by_over_10b_list)
    message = "Stocks RS rating > 80 over 10 billion\n\n"
    message += f"# of stocks: {len(filtered_by_over_10b_list)}\n\n"
    message += results       
    message = urllib.parse.quote(message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url)
    
    message = "Industry-Sectors with most RS rating > 80\n\n"
    for tup in sorted_industry_sector_dict[:10]:
        x ='\n'.join(str(tup))
        print(x)
        message += x
    message = urllib.parse.quote(message)
    url = f"https://api.telegram.org/{telegram_apikey}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url)

    
    #### read Industries RS file
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
