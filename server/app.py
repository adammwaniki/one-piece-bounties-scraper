# Import required libraries
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
#import time

# Initialize Flask application
app = Flask(__name__)

def scrape_bounties():
    page = requests.get('https://onepiece.fandom.com/wiki/Bounties/List')
    #print(page.content)
    #time.sleep(3)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

    bounty_data = {}
    current_section = None
    
    content_elements = soup.find_all(['h3', 'h4', 'h5', 'table'])

    for element in content_elements:
        if element.name in ['h3', 'h4', 'h5']:
            span = element.find('span', class_='mw-headline')
            if span:
                current_section = span.text.strip()
                bounty_data[current_section] = []
                
        elif element.name == 'table' and 'wikitable' in element.get('class', []):
            table_data = []
            rows = element.find_all('tr')
            i = 0
            
            while i < len(rows):
                cells = rows[i].find_all('td')
                if cells and len(cells) == 3:
                    entry = {
                        "name": cells[0].text.strip(),
                        "nickname": cells[1].text.replace('\"' , "").split('[')[0].strip(),
                        "bounty": cells[2].text.split('[')[0].strip()
                    }
                    
                    # Handle supplementary details in next row
                    if i + 1 < len(rows):
                        next_cells = rows[i + 1].find_all('td')
                        if next_cells:
                            entry["supplementary details"] = ' '.join([cell.text.split('[')[0].strip() for cell in next_cells])
                            i += 1  # Skip the processed next row
                            
                    table_data.append(entry)
                elif cells:
                    table_data.append([cell.text.split('[')[0].strip() for cell in cells])
                i += 1
                    
            if current_section:
                bounty_data[current_section] = table_data

    return bounty_data


# Define home route
@app.route('/')
def home():
    return jsonify({"message": "Hello One Piece fans! This is a simple API for One Piece Bounties. Check out the /bounties route for the data."})

# Define bounties route that returns all scraped data
@app.route('/bounties')
def get_bounties():
    return jsonify(scrape_bounties())

# Run the Flask application in debug mode if script is run directly
if __name__ == '__main__':
    app.run(debug=True)
