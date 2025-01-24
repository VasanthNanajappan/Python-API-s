import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from pprint import pprint

# Function to extract exchange rates from x-rates.com
def get_exchange_list_xrates(currency, amount=1):
    try:
        # Creating a connection to x-rates
        url = f"https://www.x-rates.com/table/?from={currency}&amount={amount}"
        content = requests.get(url).content
        
        # Parsing the page content
        soup = bs(content, "html.parser")
        
        # Extracting the timestamp
        elements = soup.find_all("span", attrs={"class": "ratesTimestamp"})
        price_datetime = None
        if elements:
            price_datetime = parse(elements[1].text)  # Access safely
            print("Price DateTime:", price_datetime)
        else:
            print("No elements found with the class 'ratesTimestamp'")

        # Extracting exchange rates
        exchange_table = soup.find("table", attrs={"class": "tablesorter ratesTable"})
        exchange_rates = {}

        if exchange_table:
            for tr in exchange_table.find_all("tr"):
                tds = tr.find_all("td")
                if tds and len(tds) >= 2:
                    currency_name = tds[0].text.strip()  # Clean currency name
                    exchange_rate = float(tds[1].text.strip())  # Parse the rate
                    exchange_rates[currency_name] = exchange_rate
        else:
            print("No exchange rates table found.")
        
        return price_datetime, exchange_rates
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, {}

# Test the function
if __name__ == "__main__":
    import sys
    try:
        source_currency = sys.argv[1]
        amount = float(sys.argv[2])
        target_currency = "GBP"
        
        # Fetch exchange rates
        price_datetime, exchange_rates = get_exchange_list_xrates(source_currency, amount)
        
        # Display results
        print("Last updated:", price_datetime)
        pprint(exchange_rates)
    except IndexError:
        print("Usage: python script.py <source_currency> <amount>")
