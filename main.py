import flask
from flask import request, jsonify
import urllib.request
from bs4 import BeautifulSoup

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


# TODO: add web scraper for formula 2 website.
base_url = "https://www.fiaformula2.com"

def get_latest():
    landing_page = base_url + "/Latest"
    print(landing_page)
    with urllib.request.urlopen(landing_page) as respon:
        response = respon.read()

    result = []

    soup = BeautifulSoup(response, 'html.parser')
    # articles = soup.find_all('article', attrs={"class": "article-ct"})
    # news = soup.findAll("div", {"class": "article-listing-card--item col-md-6 col-lg-4"})
    news = soup.findAll("div", {"class": lambda value: value and value.startswith("article-listing-card--item")})
    for article in news:
        link = base_url + article.find(class_="f1-cc")['href']
        thumbnail_link = article.find(class_="f1-cc--photo")['data-src']
        caption_title = article.find(class_="f1-cc--caption").find(class_="font-tag").get_text()
        caption_text = article.find(class_="f1-cc--caption").find(class_="font-text-body").get_text()
        temp = {'link': link, 'thumbnail_link': thumbnail_link, 'caption_title': caption_title, 'caption_text': caption_text}
        result.append(temp)
    return result


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Formula 2 Api</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/latest', methods=['GET'])
def api_all():
    return jsonify(get_latest())


# app.run()
