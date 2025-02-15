from flask import Flask, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup

# app = Flask(__name__)
asc_staff = Blueprint('asc_staff', __name__)

@asc_staff.route('/')
@asc_staff.route('/asc_staff', methods=['GET'])
def scrape_staff():
    try:
        # URL of the page to scrape
        url = "https://kcascension.org/about/staff/"

        # Send a GET request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for unsuccessful requests

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the article with id="post-14"
        article = soup.find(id="post-14")
        if not article:
            return jsonify({"error": "No article with id 'post-14' found"}), 404

        # Find the div with class="entry-content" inside the article
        entry_content = article.find(class_="entry-content")
        if not entry_content:
            return jsonify({"error": "No entry-content div found in the article"}), 404

        # Find all <h3> tags inside the entry content
        h3_tags = entry_content.find_all("h3", class_="wp-block-heading")

        # Initialize a list to store the extracted data
        extracted_data = []

        # Iterate through each <h3> tag
        for h3 in h3_tags:
            title = h3.get_text(strip=True)  # Extract the title from <h3>

            # Find the corresponding <section class="staffImages"> for this <h3>
            staff_section = h3.find_next("section", class_="staffImages")

            if staff_section:  # Check if staff_section exists
                # Find all <figure> tags within the staff section
                staff_members = staff_section.find_all("figure")

                # Initialize a list to store staff information
                staff_info = []

                for staff in staff_members:
                    # Extract the image src and alt text (if available)
                    img_tag = staff.find("img")
                    img_src = img_tag["data-src"] if img_tag else ""
                    img_alt = img_tag["alt"] if img_tag else ""

                    # Extract the caption (name, title, and email)
                    figcaption = staff.find("figcaption")
                    if figcaption:
                        staff_details = figcaption.get_text("\n", strip=True)
                    else:
                        staff_details = "No details"

                    # Store the staff information
                    staff_info.append({
                        "image_src": img_src,
                        "image_alt": img_alt,
                        "staff_details": staff_details
                    })

                # Store the extracted data for this section
                extracted_data.append({
                    "title": title,
                    "staff_info": staff_info
                })
            else:
                # If no staff section is found, note it
                extracted_data.append({
                    "title": title,
                    "staff_info": "No staff images available"
                })

        # Return the extracted data as JSON
        return jsonify(extracted_data)

    except Exception as e:
        # Return error details as JSON
        return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
