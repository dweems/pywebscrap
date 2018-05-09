from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import string

# Define some arrays
raw_html = []
data = []
final_data = []

# get raw html from specified URL
def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error diring request to {0} : {1}'.format(url, str(e)))
        return None

# Check the status of the URL
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

# Store the Raw HTML into an array
for letter in list(string.ascii_uppercase):
    raw_html.append(simple_get('https://webapps.jcdh.org/scores/ehfs/FoodServiceScores.aspx?Letter={}'.format(letter)))

# Iterate over the raw html and parse it with BS4
for html in raw_html:
    soup = BeautifulSoup(html, "html.parser")

    # Set the rows to a variable
    data_rows = soup.findAll('tr')[2:]

    # Iterate over the data to get the text
    business_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows)-3)]
    # Set the ~clean data to the data array
    data.append(business_data)

# Iterate over the data
for d in data:
    for score in d:
        # Make sure we have valid data
        if len(score) != 5:
            break
        # A little more sanitization plz
        score[2] = score[2].replace('\n\n', ' ')
        score[2] = score[2].replace('\n', '')
        score[2] = score[2].replace('\xa0–\xa0', ' ')
        final_data.append(score)

for x in final_data:
    print(x)
