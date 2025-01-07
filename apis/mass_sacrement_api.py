from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

# app = Flask(__name__)
asc_mass_and_sacraments = Blueprint('asc_mass_and_sacraments', __name__)


@asc_mass_and_sacraments.route('/')
@asc_mass_and_sacraments.route('/asc_mass_and_sacraments', methods=['GET'])
def scrape_calendar():
    try:
        # URL of the page
        url = "https://kcascension.org/"

        # Send a GET request to fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the calendar wrap section
        calendar_wrap = soup.find('div', id='homeBoxCalendarWrap')
        if not calendar_wrap:
            return jsonify({"error": "No div with id 'homeBoxCalendarWrap' found"}), 404

        # Find all divs with class "homeBox"
        home_boxes = calendar_wrap.find_all('div', class_='homeBox')

        # Extract data from each homeBox
        extracted_data = []
        for idx, home_box in enumerate(home_boxes, 1):
            # Extract the heading, if present
            heading = home_box.find('h3')
            heading_text = heading.get_text(strip=True) if heading else "No Heading"

            # Extract the body, if present
            body = home_box.find('div', class_='homeBoxBody')
            body_text = body.get_text(separator="\n", strip=True) if body else "No Body Content"

            # Extract the footer, if present
            footer = home_box.find('div', class_='homeBoxFoot')
            footer_text = footer.get_text(separator="\n", strip=True) if footer else "No Footer Content"

            # Append the data to the list
            extracted_data.append({
                "heading": heading_text,
                "body": body_text,
                "footer": footer_text
            })

        # Return the extracted data as JSON
        return jsonify(extracted_data)

    except Exception as e:
        # Return error details as JSON
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
