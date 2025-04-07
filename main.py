import os
import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(category='business', query=None, country='in'):
    url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={NEWS_API_KEY}'

    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}'

    response = requests.get(url)
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
    query = request.args.get("q")
    category = request.args.get("category", "business")
    news = get_news(category=category, query=query)

    return render_template("index.html", articles=news, query=query, selected_category=category)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
