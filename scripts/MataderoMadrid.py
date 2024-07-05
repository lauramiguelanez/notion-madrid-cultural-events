# importing the libraries
from bs4 import BeautifulSoup
import requests
import dateparser
from datetime import datetime
import json


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
                            date_text = date_element.find_next(text=True).strip()
                            # Split date_text into individual date components
                            date_components = [
                                date.strip() for date in date_text.split(",")
                            ]
                            # Remove any duplicates and empty strings
                            date_strings = list(set(date_components))
                            date_strings = [date for date in date_strings if date]
                            # Parse each date string into a datetime object
                            date_objects = [
                                dateparser.parse(date, languages=["es"])
                                for date in date_strings
                            ]

                            print(
                                f"Date: {date_text} ---- {date_strings} ---- {date_objects}"
                            )

                        else:
                            print("The text 'Fecha' was not found on the child page.")

                        # ADD DATA
                        data.append(
                            {
                                "url": href,
                                "event_title_text": event_title_text,
                                "date_text": date_text,
                                "date_object": date_objects,
                                #'description_text': description_text
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




def main():
    url ="https://www.mataderomadrid.org/programacion?f%5B0%5D=institution%3A25930"
    data = scrape_data(url)
    if data:
        # Specify the file path where you want to save the JSON file
        file_path = "data/MataderoMadrid.json"

        # Save the data as JSON
        with open(file_path, "w") as file:
            json.dump(data, file)

        print("Data saved successfully.")


if __name__ == "__main__":
    main()
