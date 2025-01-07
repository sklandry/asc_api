
from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

# app = Flask(__name__)
asc_trending = Blueprint('trending_bp', __name__)


@asc_trending.route('/')
@asc_trending.route('/asc_trending', methods=['GET'])
def scrape_trending():
    try:
        # URL of the page
        url = "https://kcascension.org/"

        # Send a GET request to fetch the HTML content
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            trending_data = []

            # Locate the trending div
            trending_div = soup.find('div', id='trending')
            if trending_div:
                # Locate the homeCards section inside the trending div
                home_cards_section = trending_div.find('section', id='homeCards')
                if home_cards_section:
                    # Find all <a> tags inside the homeCards section
                    links = home_cards_section.find_all('a', href=True)

                    # Extract the href and data-src attributes
                    for idx, link in enumerate(links, 1):
                        href = link['href']
                        # Find the <img> tag within the <a> tag
                        img_tag = link.find('img', {'data-src': True})
                        data_src = img_tag['data-src'] if img_tag else ""

                        trending_data.append({
                            "Card Number": idx,
                            "Link": href,
                            "ImageLink": data_src
                        })
                else:
                    return jsonify({"error": "No section with id 'homeCards' found inside 'trending'."}), 404
            else:
                return jsonify({"error": "No div with id 'trending' found."}), 404
        else:
            return jsonify({"error": f"Failed to fetch the page. Status code: {response.status_code}"}), response.status_code

        # Return the scraped data as JSON
        return jsonify(trending_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
