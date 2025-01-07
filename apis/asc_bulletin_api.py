
from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

asc_bulletin_bp = Blueprint('asc_bulletin', __name__)

@asc_bulletin_bp.route('/')
@asc_bulletin_bp.route('/asc_bulletin', methods=['GET'])
def scrape_bulletin():
    try:
        # URL of the page to scrape
        url = "https://kcascension.org/communications/bulletin/"

        # Send a GET request to fetch the HTML content
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            bulletin_data = []

            # Locate the target article and entry-content
            article_post = soup.find('article', id='post-100')
            if article_post:
                entry_content = article_post.find('div', class_='entry-content')
                if entry_content:
                    # Find all <figure> tags within the entry-content
                    figures = entry_content.find_all('figure', class_='aligncenter size-large is-resized')

                    # Extract and store href and figcaption values
                    for idx, figure in enumerate(figures, 1):
                        # Find <a> tag and its href attribute
                        a_tag = figure.find('a', href=True)
                        href = a_tag['href'] if a_tag else ""

                        # Find <figcaption> tag and extract its text
                        figcaption = figure.find('figcaption')
                        caption = figcaption.text.strip() if figcaption else ""

                        bulletin_data.append({
                            "FigureNumber": idx,
                            "Link": href,
                            "Caption": caption
                        })
                else:
                    return jsonify({"error": "No 'entry-content' div found."}), 404
            else:
                return jsonify({"error": "No article with id 'post-100' found."}), 404
        else:
            return jsonify({"error": f"Failed to fetch the page. HTTP Status Code: {response.status_code}"}), response.status_code

        # Return the scraped data as JSON
        return jsonify(bulletin_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
