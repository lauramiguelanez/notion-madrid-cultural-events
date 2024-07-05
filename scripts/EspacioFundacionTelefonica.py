from bs4 import BeautifulSoup
import requests
import dateparser
import json


def scrape_data(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for event in soup.find_all("div", class_="lista_eventos"):
            link = event.find("a")
            if link and "href" in link.attrs:
                href = link["href"]
                if not href.startswith("http"):
                    href = requests.compat.urljoin(url, href)
                # print(f"Visiting URL: {href}")

                event_response = requests.get(href)
                if event_response.status_code == 200:
                    event_soup = BeautifulSoup(event_response.content, "html.parser")

                    title_element = event_soup.find("span", class_="titulo")
                    title = title_element.get_text(strip=True)

                    description_element = event_soup.find("div", class_="info pc")
                    paragraphs = description_element.find_all("p")
                    description = "\n".join(
                        paragraph.get_text(strip=True) for paragraph in paragraphs
                    )

                    dates = []
                    for date_element in event_soup.find_all("div", class_="fecha"):
                        dia = date_element.find("div", class_="dia").get_text(
                            strip=True
                        )
                        mes = date_element.find("div", class_="mes").get_text(
                            strip=True
                        )
                        date_parsed = dateparser.parse(f"{dia} {mes}", languages=["es"])
                        dates.append(date_parsed.strftime("%d %B %Y"))

                    img_element = event.find("img")
                    image_url = img_element["src"] if img_element else None

                    data.append(
                        {
                            "url": href,
                            "name": title,
                            "description": description,
                            "dates": dates,
                            "image": image_url,
                            "organizer": "Espacio Fundación Telefónica",
                            "type": "Exhibition",
                            "price": 0,
                        }
                    )
                else:
                    print(
                        f"Failed to retrieve the child page. Status code: {event_response.status_code}"
                    )
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return data


def main():
    url = "https://espacio.fundaciontelefonica.com/agenda/exposiciones/"
    data = scrape_data(url)
    if data:
        # Specify the file path where you want to save the JSON file
        file_path = "data/EspacioFundacionTelefonica.json"

        # Save the data as JSON
        with open(file_path, "w") as file:
            json.dump(data, file)

        print("Data saved successfully.")


if __name__ == "__main__":
    main()
