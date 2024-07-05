from bs4 import BeautifulSoup
import requests
import dateparser
import json


def scrape_data(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        for event in soup.find_all("div", class_="enlace--bloque gtm-snippet-proyectos"):
            link = event.find("a")
            if link and "href" in link.attrs:
                href = link["href"]
                if not href.startswith("http"):
                    href = requests.compat.urljoin(url, href)
                print(f"Visiting URL: {href}")

                
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data


def main():
    url = "https://www.museoreinasofia.es/exposiciones"
    data = scrape_data(url)
    if data:
        file_path = "data/MuseoReinaSofia.json"

        # Save the data as JSON
        with open(file_path, "w") as file:
            json.dump(data, file)

        print("Data saved successfully.")


if __name__ == "__main__":
    main()
