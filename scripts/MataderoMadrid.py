# importing the libraries
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.parser import parse
import re
import json

def extract_date_from_text(text):
    # Diccionario para convertir nombres de meses a números
    month_to_number = {
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
        "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
        "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
    }
    
    # Lista para almacenar las fechas encontradas
    dates = []
    
    # Expresiones regulares para identificar los diferentes formatos de fecha
    patterns = [
        (r"Hasta el (\d{1,2}) de (\w+) (\d{4})", lambda day, month, year: f"{year}-{month_to_number[month]}-{day.zfill(2)}"),
        (r"Entre (\w+) y (\w+)", lambda start_month, end_month: [f"2024-{month_to_number[start_month]}-01", f"2024-{month_to_number[end_month]}-01"]),
        (r"Del (\d{1,2}) (\w+) al (\d{1,2}) (\w+) (\d{4})", lambda start_day, start_month, end_day, end_month, year: [f"{year}-{month_to_number[start_month]}-{start_day.zfill(2)}", f"{year}-{month_to_number[end_month]}-{end_day.zfill(2)}"]),
        (r"Hasta (\d{1,2}) (\w+) (\d{4})", lambda day, month, year: f"{year}-{month_to_number[month]}-{day.zfill(2)}"),
        (r"Del (\d{1,2}) al (\d{1,2}) (\w+) (\d{4})", lambda start_day, end_day, month, year: [f"{year}-{month_to_number[month]}-{start_day.zfill(2)}", f"{year}-{month_to_number[month]}-{end_day.zfill(2)}"]),
        (r"(\d{1,2}) al (\d{1,2}) (\w+) (\d{4})", lambda start_day, end_day, month, year: [f"{year}-{month_to_number[month]}-{start_day.zfill(2)}", f"{year}-{month_to_number[month]}-{end_day.zfill(2)}"]),
        (r"(\d{1,2}) de (\w+)", lambda day, month: f"2024-{month_to_number[month]}-{day.zfill(2)}"),
        (r"(\d{1,2}) (\w+) (\d{4})", lambda day, month, year: f"{year}-{month_to_number[month]}-{day.zfill(2)}")
    ]
    
    # Procesar cada patrón para encontrar coincidencias
    for pattern, formatter in patterns:
        match = re.search(pattern, text)
        if match:
            result = formatter(*match.groups())
            # Si el resultado es una lista (rango de fechas), extender la lista de fechas
            if isinstance(result, list):
                dates.extend(result)
            else:
                dates.append(result)
            break
    
    return dates


def scrape_data(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # List to store the gathered information
    data = []
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with class "view-content"
        view_content_div = soup.find("div", class_="view-content")

        # Check if the div was found
        if view_content_div:
            # Iterate over each child element of the div
            for child in view_content_div.find_all(recursive=False):
                # Find the link in the child element (assuming it's an <a> tag)
                link = child.find("a")
                if link and "href" in link.attrs:
                    href = link["href"]
                    # If the href is relative, convert it to absolute
                    if not href.startswith("http"):
                        href = requests.compat.urljoin(url, href)
                    # print(f"......Visiting URL: {href}")

                    # Send a GET request to the child link
                    child_response = requests.get(href)
                    if child_response.status_code == 200:
                        # Parse the content of the child page with BeautifulSoup
                        child_soup = BeautifulSoup(child_response.content, "html.parser")

                        # TITLE ind the element with class "group-top" and get its text
                        event_title_element = child_soup.find(class_="group-top")
                        if event_title_element:
                            first_child = event_title_element.find(recursive=False)
                            event_title_text = first_child.get_text(strip=True)
                            # print(f"Text from 'group-top' element: {event_title_text}")
                        else:
                            print(
                                "The element with class 'group-top' was not found on the child page."
                            )

                        # DATE
                        date_element = child_soup.find(text="Fecha")
                        if date_element:
                            # Get the next sibling text
                            date_text = date_element.find_next(string=True).strip()
                            date_list = extract_date_from_text(date_text)
                            # print(date_text,"-----", date_list)
                            

                        else:
                            print("The text 'Fecha' was not found on the child page.")
                            
                        # GET IMAGE
                        # Get div element with class "field--name-image"
                        image_div = child_soup.find("div", class_="field--name-image")
                        if image_div:
                            # Find the image tag within the div
                            image_tag = image_div.find("img")
                            if image_tag and "src" in image_tag.attrs:
                                image_url = "https://www.mataderomadrid.org/" + image_tag["src"]
                                # print(f"Image URL: {image_url}")
                            else:
                                print("Image tag or 'src' attribute not found.")
                        else:
                            print("Div with class 'field--name-image' not found.")
                            
                        # GET DESCRIPTION
                        # Get the text from the element with class "field--name-field-teaser"
                        description_element = child_soup.find(class_="field--name-field-teaser")
                        if description_element:
                            description_text = description_element.get_text(strip=True)
                            # print(f"Description: {description_text}")
                        else:
                            print("The element with class 'field--name-field-teaser' was not found on the child page.")

                        # ADD DATA
                        data.append(
                            {
                                "url": href,
                                "name": event_title_text,
                                "description": description_text,
                                "dates": date_list,
                                "image": image_url,
                                "organizer": "Matadero Madrid",
                                "type": "Exhibition",
                                "price": 0,
                            }
                        )

                    else:
                        print(
                            f"Failed to retrieve the child page. Status code: {child_response.status_code}"
                        )

        else:
            print("The div with class 'view-content' was not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return data


def main():
    url ="https://www.mataderomadrid.org/programacion?f%5B0%5D=institution%3A25930"
    data = scrape_data(url)
    if data:
        # Specify the file path where you want to save the JSON file
        file_path = "data/MataderoMadrid.json"
        
        print(data)
        # Save the data as JSON
        with open(file_path, "w") as file:
            json.dump(data, file)

        print("Data saved successfully.")


if __name__ == "__main__":
    main()




