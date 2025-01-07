from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


# Turning the url to be scraped into a variable and using BeautifulSoup to parse the HTML
page=requests.get('https://quotes.toscrape.com/')
soup=BeautifulSoup(page.content, 'html.parser')

# Creating a list of dictionaries of the scraped data
data = []
for i in range(0, 10):
    author = soup.find_all('small', class_='author')[i].text.strip()
    # Removing the Unicode escape sequences representing curly quotation marks
    quote = soup.find_all('div', class_='quote')[i].find('span', class_='text').text.strip().replace('\u201c', '').replace('\u201d', '')
    tag = [tag.text.strip() for tag in soup.find_all('div', class_='tags')[i].find_all('a', class_='tag')]
    data.append({
        'quote': quote,
        'author': author,
        'tags': tag
    })


@app.route('/')
def home():
    return jsonify({"message": "Hello One Piece fans!"})

# Creating a route to return the scraped data
@app.route('/quotes')
def get_quotes():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
