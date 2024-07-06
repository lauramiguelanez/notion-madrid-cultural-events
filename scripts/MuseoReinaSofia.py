from bs4 import BeautifulSoup
import requests
import dateparser
import json
import datetime


def scrape_data(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        articles = soup.find_all("article")
        for article in articles:
            # Process each article element as needed
            a_element = article.find("a")
            if a_element:
                href = a_element.get("href")
                if href:
                    # Go to the page and process the data
                    page_url = f"https://www.museoreinasofia.es{href}"
                    page_response = requests.get(page_url)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, "html.parser")
                        titulo_element = page_soup.find(class_="titulo")
                        subtitulo_element = page_soup.find(class_="subtitulo")

                        # NAME
                        if titulo_element and subtitulo_element:
                            titulo_text = titulo_element.get_text(strip=True)
                            subtitulo_text = subtitulo_element.get_text(strip=True)
                            title = titulo_text + ". " + subtitulo_text
                            
                        else:
                            print("Failed to find titulo or subtitulo element.")
                        
                        # IMAGE
                        image_element = page_soup.find(class_="cuerpo-ficha--figure")
                        if image_element:
                            img_element = image_element.find("img")
                            if img_element:
                                image_url = img_element.get("src")
                            else:
                                print("Failed to find img element.")
                                
                        # DESCRIPTION
                        description_element = page_soup.find(class_="field-name-field-exposicion-texto")
                        if description_element:
                            p_elements = description_element.find_all("p")
                            description = " ".join([p.get_text(strip=True) for p in p_elements])
                        else:
                            print("Failed to find description element.")
                            
                        # DATES
                        date_element = page_soup.find(class_="fecha")
                        if date_element:
                            date_text = date_element.get_text(strip=True).replace("de ", "")
                            
                            year = date_text.split(", ")[-1]
                            dates = date_text.split(" - ")
                            dates = [date.split(", ")[0] + f" {year}" for date in dates]
                            iso_dates = []
                            for date in dates:
                                parsed_date = dateparser.parse(date, languages=["es"])
                                iso_date = parsed_date.strftime("%Y-%m-%d")
                                iso_dates.append(iso_date)
                
                        data.append(
                            {
                                "url": page_url,
                                "name": title,
                                "description": description,
                                "dates": iso_dates,
                                "image": image_url,
                                "organizer": "Museo Reina Sofía",
                                "type": "Exhibition",
                                "price": 0,
                            }
                        )    
                       
                    else:
                        print(f"Failed to retrieve the page. Status code: {page_response.status_code}")
                
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
