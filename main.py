import flask
from flask import jsonify
import urllib.request
from bs4 import BeautifulSoup

app = flask.Flask(__name__)
# app.config["DEBUG"] = True


# TODO: add web scraper for formula 2 website.
base_url = "https://www.fiaformula2.com"


# retrieves a list of latest articles
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


# retrieves all details of the given article
def get_news(link):
    with urllib.request.urlopen(link) as respon:
        response = respon.read()

    soup = BeautifulSoup(response, 'html.parser')

    # text retrieval
    news = soup.findAll("div", {"class": "rich-text font-text-body"})
    text = ""
    for paragraph in news:
        text = text + paragraph.get_text()

    # image retrieval
    images = soup.findAll("div", {"class": "f1-image--parent"})
    img = []
    for i in images:
        img.append(i.findAll("img")[0]['data-src'])

    # video retrieval
    video = soup.findAll("div", {"class": "video-player"})
    vdo = []
    for v in video:
        li = v.findAll("source")[0]['src']
        t = v.findAll("video")[0]['poster']
        temp = {'video_thumb': t, 'video_link': li}
        vdo.append(temp)

    # image gallery retrieval
    img_g = soup.findAll("div", {"class": "react-images__view-wrapper"})
    img_gal = []
    for i in img_g:
        img = i.findAll("img")[0]['src']
        img_gal.append(img)

    result = {'text': text, 'images': img, 'videos': vdo, 'img_gallery': img_gal}

    return result


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Formula 2 Api</h1>'''


@app.route('/api/v1/latest', methods=['GET'])
def api_all():
    return jsonify(get_latest())


@app.route('/api/v1/news/<path:encoded_url>', methods=['GET'])
def api_news(encoded_url):
    link = encoded_url
    return jsonify(get_news(link))

# app.run()
