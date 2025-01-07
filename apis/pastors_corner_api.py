
from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

# app = Flask(__name__)
# @app.route('/')
pastor_corner = Blueprint('pastor_corner', __name__)
@pastor_corner.route('/')
@pastor_corner.route('/pastor_corner', methods=['GET'])
def scrape_blog():
    try:
        # URL to scrape
        url = "https://kcascension.org/communications/blog/"

        eventsPastorCorner = []
        # Send a GET request
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the blog posts section
            articles = soup.find_all("article", class_="entry")

            for article in articles:
                # Get the article title and URL
                title_tag = article.find("h2", class_="entry-title").find("a")
                title = title_tag.text.strip() if title_tag else ""
                href = title_tag["href"] if title_tag else ""

                # Get the content in the <p> tag inside the body
                excerpt_tag = article.find("div", class_="entry-article-body").find("p")
                excerpt = excerpt_tag.text.strip() if excerpt_tag else ""

                # Append the data to the list
                eventsPastorCorner.append({
                    "Title": title,
                    "URL": href,
                    "Detail": excerpt
                })
        else:
            return jsonify({"error": f"Failed to fetch the page. Status code: {response.status_code}"}), response.status_code

        # Return the scraped data as JSON
        return jsonify(eventsPastorCorner)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
