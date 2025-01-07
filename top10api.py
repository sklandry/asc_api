from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
import base64

# app = Flask(__name__)
# 
asc_top_10 = Blueprint('asc_top_10', __name__)
@asc_top_10.route('/')
@asc_top_10.route('/asc_top_10', methods=['GET'])
def scrape_top_10():
    try:
        # URL to scrape
        url = "https://kcascension.org/"
        events = []

        # Fetch the webpage
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the section with id="top-10"
            top_10_section = soup.find('section', id='top-10')

            if top_10_section:
                # Extract all <figure> tags
                figures = top_10_section.find_all('figure')

                # Loop through and extract image and link information
                for figure in figures:
                    # Find the anchor tag (<a>)
                    link_tag = figure.find('a')
                    link_url = link_tag['href'] if link_tag else ""

                    # Find the image tag (<img>)
                    img_tag = figure.find('img')
                    img_src = img_tag.get('data-src') or img_tag.get('src') if img_tag else ""
                    img_alt = img_tag['alt'] if img_tag else ""

                    events.append({
                        "imageUrl": img_src,
                        "detailsLink": link_url,
                        "imageAlt": img_alt
                    })
            else:
                return jsonify({"error": "Section with id='top-10' not found on the page."}), 404
        else:
            return jsonify({"error": f"Failed to fetch the webpage. Status code: {response.status_code}"}), response.status_code

        # Return the events as a JSON response
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/save_image', methods=['GET'])
# def save_image():
#     try:
#         # Base64 string
#         base64_string = "R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

#         # Decode and save to file
#         img_data = base64.b64decode(base64_string)
#         file_path = "image.gif"
#         with open(file_path, "wb") as f:
#             f.write(img_data)

#         return jsonify({"message": f"Image saved as {file_path}"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     # app.run(host='10.0.2.2', port=8000, debug=True)
#     app.run(host='0.0.0.0', port=8000, debug=True)

