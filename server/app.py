# Import required libraries
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

# Initialize Flask application
app = Flask(__name__)

def scrape_bounties():
    # Fetch the One Piece bounties webpage
    page = requests.get('https://onepiece.fandom.com/wiki/Bounties/List')
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Initialize data structures to store bounty information
    bounty_data = {}
    current_h3_section = None
    current_h4_section = None

    # Find all h3, h4 headers and tables in the page
    content_elements = soup.find_all(['h3', 'h4', 'table'])

    # Process each element found
    for element in content_elements:
        # Handle h3 headers (main sections)
        if element.name == 'h3':
            span = element.find('span', class_='mw-headline')
            if span and span.find('a'):
                current_h3_section = span.find('a').text.strip()
                bounty_data[current_h3_section] = {}
                current_h4_section = None
        
        # Handle h4 headers (subsections)
        elif element.name == 'h4':
            span = element.find('span', class_='mw-headline')
            if span and span.find('a') and current_h3_section:
                current_h4_section = span.find('a').text.strip()
                if isinstance(bounty_data[current_h3_section], dict):
                    bounty_data[current_h3_section][current_h4_section] = []
        
        # Handle tables containing bounty information
        elif element.name == 'table' and 'wikitable' in element.get('class', []):
            table_data = []
            # Process each row in the table
            for row in element.find_all('tr'):
                cells = row.find_all('td')
                # Handle 3-column rows (Name, Nickname, Bounty)
                if cells and len(cells) == 3:
                    table_data.append({
                        "Name": cells[0].text.strip(),
                        "Nickname": cells[1].text.strip(),
                        "Bounty": cells[2].text.strip()
                    })
                # Handle other row formats
                elif cells:
                    table_data.append([cell.text.strip() for cell in cells])
            
            # Store table data in appropriate section
            if current_h4_section and current_h3_section and isinstance(bounty_data[current_h3_section], dict):
                bounty_data[current_h3_section][current_h4_section] = table_data
            elif current_h3_section:
                bounty_data[current_h3_section] = table_data

    return bounty_data

# Define home route
@app.route('/')
def home():
    return jsonify({"message": "Hello One Piece fans!"})

# Define bounties route that returns all scraped data
@app.route('/bounties')
def get_bounties():
    return jsonify(scrape_bounties())

# Run the Flask application in debug mode if script is run directly
if __name__ == '__main__':
    app.run(debug=True)
