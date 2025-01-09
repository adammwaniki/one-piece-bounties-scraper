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

## Technologies Used

- Python
- Flask
- BeautifulSoup4
- Requests

## Setup and Installation

1. Clone the repository:
```bash```
git clone https://github.com/adammwaniki/one-piece-bounties-scraper.git


2. Install dependencies:
```bash```
pip install flask beautifulsoup4 requests


3. Run the application:
```bash```
cd one-piece-bounties-scraper/server
source onePiece/bin/activate
python3 app.py

-The server will start on http://localhost:5000

## Sample Response
```json```
{
    "Section Name": {
        "Subsection Name": [
            {
                "Name": "Character Name",
                "Nickname": "Character Nickname",
                "Bounty": "Bounty Amount"
            },
            [
                "Additional Information"
            ]
        ]
    }
}

"Emperors": {
    "Beasts Pirates": [
      {
        "Bounty": "4,611,100,000",
        "Name": "Kaidou",
        "Nickname": "of the Beasts"
      },
      [
        "First Bounty: Kaidou received his first bounty of 70,000,000 around the age of 13, after escaping from a Marine ship.Current Bounty: Kaidou's current bounty is 4,611,100,000, and currently the highest known active bounty."
      ],
      {
        "Bounty": "1,390,000,000",
        "Name": "King",
        "Nickname": "The Conflagration"
      },
      [
        "As one of the three Disasters, he is one of Kaidou's right-hand men. Being the only surviving lunarian may have also influenced it."
      ],
    ]
}

## Contributing
Feel free to open issues and submit pull requests to improve the project.


## Acknowledgments
Data sourced from One Piece Fandom Wiki