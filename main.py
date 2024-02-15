import os
import requests
from dotenv import load_dotenv

# .env file contains api keys in the format of API_KEY="xxxxxx"
load_dotenv()  # take environment variables from .env.


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

alpha_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ['TW_AUTH_TOKEN'],
}

# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo

data = requests.get(url=STOCK_ENDPOINT, params=alpha_parameters)
data.raise_for_status()
quote = data.json()

qdata = quote["Time Series (Daily)"]
qdict = {key: value['4. close'] for (key, value) in qdata.items()}
print(qdict)
yesterday_date = list(qdict.keys())[0]
print(yesterday_date)
yesterday_close =(list(qdict.values())[0])
print (yesterday_close)
day_before_yest_close = (list(qdict.values())[1])
print (day_before_yest_close)
diff_change = abs(float(yesterday_close) - float(day_before_yest_close))/float(day_before_yest_close)
print(diff_change)
if diff_change > 0.05:
    print("Get News")
else:
    print("No News")




## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# url = ('https://newsapi.org/v2/everything?'
#        'q=Tesla&'
#        'from=2024-02-15&'
#        'sortBy=popularity&'
#        'apiKey=XXXXXx')

news_parameters = {
    "q": COMPANY_NAME.split(" ")[0],
    "from": yesterday_date,
    "sortBy": "relevancy",
    "Language":"en",
    "pageSize": 3,
    "apikey": os.environ['NEWS_API_KEY'],
}

news_data = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
news_data.raise_for_status()
news = news_data.json()
articles_list = news["articles"]
titles_list = [articles_list[0]["title"], articles_list[1]["title"], articles_list[2]["title"]]
print(titles_list)


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
