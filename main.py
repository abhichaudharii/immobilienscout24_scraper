import requests
from bs4 import BeautifulSoup

cookies = {
    'reese84': 'GET_COOKIES_USING_YOUR_BROWSER_SELECT_reese84_AND_COPY_PASTE_THE_VALUES_HERE',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
}

def get_property_links(url:str):
    print(f"[I] GETTING PROPERTY LINKS FROM URL: {url}")
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        result_dict = {}
        # Parse the HTML content using BeautifulSou 
        print("[+] GOT A VALID RESPONSE FROM SERVER")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all property listings on the page
        property_listings = soup.find_all('li', class_='result-list__listing')
        print(f"[+] GOT {len(property_listings)} LISTING")
        total_page_count = soup.find_all('li', class_='p-items')[-2].text.strip()
        print(total_page_count)
        result_dict["total_page_count"] = total_page_count

        # Iterate over each property listing
        for idx, listing in enumerate(property_listings):
            # Extract property details
            data = {}

            title = listing.find('h2')
            if title is not None:
                title = title.text.strip()
            else:
                title =""
            
            address = listing.find('div', class_='result-list-entry__address')
            if address is not None:
                address = address.text.strip()
            else:
                address =""


            price = listing.find('dl', class_='grid-item result-list-entry__primary-criterion')
            if price is not None:
                price = price.text.split(" ")[0].strip() + "€"

            property_url = 'https://www.immobilienscout24.de'
            if property_url is not None:
                property_url = property_url + listing.find('a')['href']

            data["title"] = title
            data["address"] = address
            data["price"] = price
            data["href"] = property_url
            result_dict[idx] = data

        return result_dict
    else:
        print(f"[!] INVALID REPONSE FROM SERVER: {response.status_code}", response.content)

def get_property_details(property_url:str):
    print(f"[I] GETTING PROPERTY DETAILS FROM URL: {property_url}")
    response = requests.get(property_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSou 
        print("[+] GOT A VALID RESPONSE FROM SERVER")
        soup = BeautifulSoup(response.content, 'html.parser')
        result_dict = {}

        # Find all property listings on the page
        title = soup.find('h1')
        if title is not None:
            result_dict["title"] = title.text.strip()
        else:
            result_dict["title"] = ""

        address = soup.find('div', class_="address-block")
        if address is not None:
            result_dict["address"] = address.text.strip()
        else:
            result_dict["address"] = ""

        coldApartmentPrice = soup.find('div', class_="is24qa-kaltmiete-main")
        if coldApartmentPrice is not None:
            result_dict["coldApartmentPrice"] = coldApartmentPrice.text.strip()
        else:
            result_dict["coldApartmentPrice"] = ""

        warmApartmentPrice = soup.find('div', class_="is24qa-warmmiete-main")
        if warmApartmentPrice is not None:
            result_dict["warmApartmentPrice"] = warmApartmentPrice.text.strip()
        else:
            result_dict["warmApartmentPrice"] = ""

        rooms = soup.find('dd', class_="is24qa-zimmer")
        if rooms is not None:
            rooms["rooms"] = rooms.text.strip()
        else:
            result_dict["rooms"] = ""

        area = soup.find('dd', class_="is24qa-wohnflaeche-ca")
        if area is not None:
            area["area"] = area.text.strip()
        else:
            result_dict["area"] = ""

        return result_dict

def main():
    url = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?pagenumber=3'
    # This gets all the properties data from passed property search url.
    property_links = get_property_links(url)
    print(property_links)

    property_url = "https://www.immobilienscout24.de/expose/143254762"
    # This get property data directly from property url
    print(get_property_details(property_url))

if __name__ == '__main__':
    main()