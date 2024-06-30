from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import socket
import dns.resolver
from urllib.parse import urlparse, urljoin

app = Flask(__name__)


app = Flask(__name__)

@app.route('/')
def home():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        domain_info = get_domain_info(url)
        subdomains = get_subdomains(url)
        assets = get_assets(url)

        return jsonify({
            'info': domain_info,
            'subdomains': subdomains,
            'asset_domains': assets
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_domain_info(url):
    hostname = url.split('//')[-1].split('/')[0]
    ip = socket.gethostbyname(hostname)
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    data = response.json()
    
    return {
        "ip": data.get("ip"),
        "isp": data.get("org"),
        "organization": data.get("org"),
        "asn": data.get("asn"),
        "location": data.get("country")
    }

def get_subdomains(url):
    # Example of subdomain retrieval using a DNS service
    hostname = url.split('//')[-1].split('/')[0]
    subdomains = []

    try:
        answers = dns.resolver.resolve('_services._dns-sd._udp.' + hostname, 'PTR')
        for rdata in answers:
            subdomains.append(rdata.to_text())
    except Exception as e:
        print(f"Error fetching subdomains: {str(e)}")

    return subdomains

def get_assets(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    assets = {
        "javascripts": [],
        "stylesheets": [],
        "images": [],
        "iframes": [],
        "anchors": []
    }

    for script in soup.find_all('script', src=True):
        src = urljoin(url, script['src'])
        domain = urlparse(src).netloc
        if domain not in assets['javascripts']:
            assets['javascripts'].append(domain)

    for link in soup.find_all('link', rel='stylesheet'):
        href = urljoin(url, link['href'])
        domain = urlparse(href).netloc
        if domain not in assets['stylesheets']:
            assets['stylesheets'].append(domain)

    for img in soup.find_all('img', src=True):
        src = urljoin(url, img['src'])
        domain = urlparse(src).netloc
        if domain not in assets['images']:
            assets['images'].append(domain)

    for iframe in soup.find_all('iframe', src=True):
        src = urljoin(url, iframe['src'])
        domain = urlparse(src).netloc
        if domain not in assets['iframes']:
            assets['iframes'].append(domain)

    for a in soup.find_all('a', href=True):
        href = urljoin(url, a['href'])
        domain = urlparse(href).netloc
        if domain not in assets['anchors']:
            assets['anchors'].append(domain)

    return assets

if __name__ == '__main__':
    app.run(debug=True)
