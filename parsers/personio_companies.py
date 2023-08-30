import requests
import xml.etree.ElementTree as ET
import xmltodict

ENDPOINT = "https://{company}.jobs.personio.de/xml?language=en"
COMPANIES = ["recup","ostrom", "gridx"]

def get_jobs(company):
    company_endpoint = ENDPOINT.format(company=company)
    # Sending the GET request
    response = requests.get(company_endpoint)

    # Checking if the request was successful (200 OK)
    if response.status_code == 200:
        # Parsing the XML content
        xml_content = response.content
        root = ET.fromstring(xml_content)
        positions = root.findall("position")

        # Abort if no positions found
        if len(positions) == 0:
            print("Request for {company} returned no positions")

        # Unpack position information and drop job description
        for p in positions:
            position_string = ET.tostring(p, encoding="utf-8").decode("utf-8")
            position_dict = xmltodict.parse(position_string)['position']
            position_dict.pop('jobDescriptions')
            print(position_dict)

    else:
        print("Request for {company} failed with status code: {response.status_code}")

if __name__ == "__main__":
    for company in COMPANIES:
        print(f"Fetching jobs for {company}")
        get_jobs(company)