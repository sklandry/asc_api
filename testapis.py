from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
@app.route('/')

@app.route('/scrape_blog', methods=['GET'])
def scrape_blog():
    try:
        url = "https://kcascension.org/communications/blog/"
        eventsPastorCorner = []

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("article", class_="entry")

            for article in articles:
                title_tag = article.find("h2", class_="entry-title").find("a")
                title = title_tag.text.strip() if title_tag else "No title"
                href = title_tag["href"] if title_tag else "No URL"

                excerpt_tag = article.find("div", class_="entry-article-body").find("p")
                excerpt = excerpt_tag.text.strip() if excerpt_tag else "No content"

                eventsPastorCorner.append({
                    "Title": title,
                    "URL": href,
                    "Detail": excerpt
                })

            with open('eventsPastorCorner.json', 'w') as json_file:
                json.dump(eventsPastorCorner, json_file, indent=4)

            return jsonify({"message": "Blog posts scraped successfully and saved to eventsPastorCorner.json"})
        else:
            return jsonify({"message": f"Failed to fetch the page. Status code: {response.status_code}"})
    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"})

@app.route('/scrape_bulletin', methods=['POST'])
def scrape_bulletin():
    try:
        url = "https://kcascension.org/communications/bulletin/"
        bulletin_data = []

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article_post = soup.find('article', id='post-100')

            if article_post:
                entry_content = article_post.find('div', class_='entry-content')
                if entry_content:
                    figures = entry_content.find_all('figure', class_='aligncenter size-large is-resized')

                    for figure in figures:
                        a_tag = figure.find('a', href=True)
                        href = a_tag['href'] if a_tag else "No href found"

                        figcaption = figure.find('figcaption')
                        caption = figcaption.text.strip() if figcaption else "No caption found"

                        bulletin_data.append({
                            "Link": href,
                            "Caption": caption
                        })

                    with open('bulletinData.json', 'w') as json_file:
                        json.dump(bulletin_data, json_file, indent=4)

                    return jsonify({"message": "Bulletin data scraped successfully and saved to bulletinData.json"})
                else:
                    return jsonify({"message": "No 'entry-content' div found."})
            else:
                return jsonify({"message": "No article with id 'post-100' found."})
        else:
            return jsonify({"message": f"Failed to fetch the page. Status code: {response.status_code}"})
    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
