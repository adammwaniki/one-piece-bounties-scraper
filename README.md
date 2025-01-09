# One Piece Bounties Scraper

A Flask-based web scraper that extracts and serves bounty information from the One Piece universe.

## Features

- Scrapes bounty data from the official One Piece Fandom Wiki
- Organizes bounties by sections and subsections
- Provides clean JSON API endpoints
- Returns structured data including character names, nicknames, and bounty amounts

## API Endpoints

- `GET /` - Welcome message for One Piece fans
- `GET /bounties` - Returns complete bounty data in JSON format
- `GET /character/<name or nickname>` - Returns bounty data for a specific character

## Technologies Used

- Python
- Flask
- BeautifulSoup4
- Requests

## Setup and Installation

1. Clone the repository:
```bash```
git clone https://github.com/adammwaniki/one-piece-bounties-scraper.git


2. Navigate to the project directory:
```bash```
- cd one-piece-bounties-scraper/server


3. Activate the virtual environment:
```bash```
source onePiece/bin/activate


4. Install dependencies:
```bash```
pip install -r requirements.txt


5. Run the application:
```bash```
- python3 app.py
    or
- python3 -m flask run

- The server will start on http://localhost:5000


## Sample Response
```json```
{

    "Crew Name": [
        {
            "bounty": "Bounty Amount",
            "name": "Character Name",
            "nickname": "Character Nickname",
            "supplementary details": "Additional information"
        },
    ]
}

```example```

{
    "Beasts Pirates": [
        {
        "bounty": "4,611,100,000",
        "name": "Kaidou",
        "nickname": "of the Beasts",
        "supplementary details": "First Bounty: Kaidou received his first bounty of 70,000,000 around the age of 13, after escaping from a Marine ship."
        },
        {
        "bounty": "1,390,000,000",
        "name": "King",
        "nickname": "The Conflagration",
        "supplementary details": "As one of the three Disasters, he is one of Kaidou's right-hand men. Being the only surviving lunarian may have also influenced it."
        },
        .
        .
        .

    ]
}

## Contributing
Feel free to open issues and submit pull requests to improve the project.


## Acknowledgments
Data sourced from One Piece Fandom Wiki