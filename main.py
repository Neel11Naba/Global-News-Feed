import os
import requests
from flask import Flask, render_template, request, jesonify
from datetime import datetime

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PAGE_SIZE = 8 # number of article per page

def get_news(query=None, page=1, country='us'):
    url = 'https://newsapi.org/v2/everything"
     params{
         "q": query or "indian stock market",
         "language": "en",
         "sortBy": "publishAt",
         "apikey": NEWS_API_KEY,
         "pageSize": PAGE_SIZE,
         "page": page
     }

    if query:
        url = 'https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}'

    response = requests.get(url,params=params)
    data = response.json()

    articles = []
    if data.get("status") == "ok":
        for article in data.get("articles", []):
            articles.append({
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'image': article.get('urlToImage'),
                'published': format_datetime(article.get('publishedAt')),
                'source': article.get('source', {}).get('name'),
            })
    return articles

def format_datetime(date_str):
    if not date_str:
        return ''
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%d %b %Y, %I:%M %p")

@app.route("/", methods=["GET", "POST"])
def home():
    articles = get_news(page=1)
    return
render_template("index.html", articles = articles)

@app.route('/load_more')
def load_more():
 page = int(request.args.get("page",1))
articles = get_news(page = page)
return jesonify(articles)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
