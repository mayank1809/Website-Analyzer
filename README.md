# Website Analyzer Flask Application

This Flask application analyzes a given website URL to provide domain information, subdomains, and asset domains such as JavaScripts, stylesheets, images, iframes, and anchor tags.

## Features

- Retrieves and displays IP address, ISP, ASN, location (country), and organization information of the domain.
- Finds and lists subdomains associated with the domain.
- Identifies and categorizes external domains used for JavaScripts, stylesheets, images, iframes, and anchor tags on the analyzed website.

## Usage 

1- Start the Flask application
python app.py

2-Open a web browser and navigate to http://127.0.0.1:5000/?url=<website-url> where <website-url> is the URL you want to analyze.

3-Alternatively, use curl from the command line:
curl "http://127.0.0.1:5000/?url=<website-url>"

Replace <website-url> with the URL you want to analyze, such as https://www.example.com.


## Prerequisites and Deployment link

deploy link- https://website-analyzer-nrhzwchifhcavlwer7xhfm.streamlit.app/

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- requests
- BeautifulSoup4
- dnspython

You can install the required Python packages using pip:

```bash
pip install -r requirements.txt
