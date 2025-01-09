# Import required libraries
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from models import Database

# Initialize Flask application
app = Flask(__name__)
db = Database()

def scrape_bounties():
    page = requests.get('https://onepiece.fandom.com/wiki/Bounties/List')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Initialize variables
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

# Define character route that returns bounty data for a specific character
@app.route('/character/<search_term>')
def find_character(search_term):
    bounties = scrape_bounties()
    found_characters = []
    
    # Search through all sections
    for section, characters in bounties.items():
        for character in characters:
            if isinstance(character, dict):  # Ensure we're dealing with character entries
                # Check if search term matches name or nickname (case insensitive)
                if search_term.lower() in character['name'].lower() or search_term.lower() in character['nickname'].lower():
                    character['section'] = section  # Add section info to result
                    found_characters.append(character)
    
    if found_characters:
        return jsonify({
            "found": len(found_characters),
            "characters": found_characters
        })
    
    return jsonify({
        "message": f"No character found with name or nickname matching '{search_term}'",
        "found": 0
    }), 404

# Define crew route that returns bounty data for a specific crew
@app.route('/crew/<crew_name>')
def find_crew(crew_name):
    bounties = scrape_bounties()
    
    # Search through all sections for crew name match
    for section_name, characters in bounties.items():
        if crew_name.lower() in section_name.lower():
            # Calculate total crew bounty
            total_bounty = 0
            for member in characters:
                if isinstance(member, dict) and 'bounty' in member:
                    # Clean and convert bounty string to number
                    bounty_str = member['bounty'].replace('\u20bd', '').replace(',', '').strip()
                    try:
                        bounty_num = int(bounty_str)
                        total_bounty += bounty_num
                    except ValueError:
                        continue
            
            return jsonify({
                "crew_name": section_name,
                "member_count": len(characters),
                "total_crew_bounty": f"{total_bounty:,}",
                "members": characters
            })
    
    return jsonify({
        "message": f"No crew found with name '{crew_name}'",
        "found": 0
    }), 404

# Define refresh route that updates the database with the latest data
@app.route('/refresh-data')
def refresh_data():
    bounties = scrape_bounties()
    db.store_bounties(bounties)
    return jsonify({"message": "Database updated successfully"})

if __name__ == '__main__':
    db.init_db()  # Creates characters table
    bounties = scrape_bounties()
    db.store_bounties(bounties)  # Stores characters and then creates/populates crews table
    app.run(debug=True)

