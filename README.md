# Automated Madrid Cultural Events in Notion

Welcome to the Automated Madrid Cultural Events project! This project scrapes websites of museums, cinemas, and other cultural institutions in Madrid to gather information about events and stores them in a Notion database for easy display and access.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Institutions](#institutions)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Event Data Schema](#event-data-schema)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Madrid Cultural Events is a Node.js-based project that runs Python scraping scripts to collect information about cultural events happening in Madrid. The collected data is stored in a Notion database, providing a centralized location to view all events.

## Features

- Scrapes event data from various cultural institutions in Madrid
- Stores event data in a Notion database
- Easy-to-use command-line interface
- FUTURE: Automated scheduling of scraping tasks

## Institutions

The project retrieves events from the following institutions:

- [Matadero Madrid](https://www.mataderomadrid.org)
- [Espacio Fundación Telefónica](https://espacio.fundaciontelefonica.com)
- FUTURE: [Cine Doré](https://www.culturaydeporte.gob.es/cultura/areas/cine/mc/cine-dore/sala-1.html)
- FUTURE: [Cines Embajadores](https://cinesembajadores.com)
- FUTURE: [Cineteca Matadero](https://www.cinetecamadrid.com)
- FUTURE: [Museo Reina Sofía](https://www.museoreinasofia.es)
- FUTURE: [Foto España](https://www.phe.es)
- FUTURE: [Museo del Prado](https://www.museodelprado.es)

## Installation

To get started with the Madrid Cultural Events project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/lauramiguelanez/notion-madrid-cultural-events.git
   cd notion-madrid-cultural-events
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper and store the events in the Notion database, use the following command:

```bash
python main.py
```

You can also schedule the scraping tasks to run at specific intervals using a task scheduler like cron (Linux/macOS) or Task Scheduler (Windows).

## Configuration

Before running the scraper, you need to configure your Notion database and update the configuration file with your Notion API key and database IDs.

Create a Notion integration and obtain your Notion API key. Follow the instructions in the Notion API documentation: Notion API Documentation

Create new databases in Notion to store the events and organizers. Note the database IDs from the URLs.

Create a .env file in the project directory and add the following variables with your Notion API key and database IDs:

```
NOTION_INTEGRATION_TOKEN=your_notion_integration_token
NOTION_EVENTS_DATABASE_ID=your_NOTION_EVENTS_DATABASE_ID
NOTION_ORGANIZER_DATABASE_ID=your_notion_organizer_database_id
```

Make sure your .env file is included in the .gitignore file to avoid committing sensitive information to your repository.

## Event Data Schema

- **Name:** Text

  - _Description:_ The name/title of the event.

- **State:** Select (Enum)

  - _Options:_ Not Planned, Will go, Went
  - _Description:_ Current state of the event (planning, attending, completed).

- **Organizer:** Relation (to Organizer database)

  - _Description:_ Reference to the organizer of the event.

- **URL:** URL

  - _Description:_ Link to the event's webpage or relevant external site.

- **Type:** Select (Enum)

  - _Options:_ Theater, Outside, Event, Excursion, Party, Drink, Eat, Exhibition, Cinema, Concert, Conference
  - _Description:_ Type/category of the event.

- **Date:** Date (Start and End dates)

  - _Description:_ Start and end dates/times of the event.

- **Image:** URL

  - _Description:_ URL link to an image related to the event.

- **Tags:** Multi-select (List of text tags)

  - _Description:_ Descriptive tags associated with the event.

- **Price:** Number

  - _Description:_ Cost or price associated with attending the event.

- **Location:** URL

  - _Description:_ URL link to Google Maps or another map service showing the event location.

- **Description:** Text
  - _Description:_ Detailed description or information about the event.

## Contributing

If you'd like to contribute, please fork the repository and create a pull request with your changes.

- Fork the repository
- Create a new branch (git checkout -b feature-branch)
- Make your changes
- Commit your changes (git commit -m 'Add some feature')
- Push to the branch (git push origin feature-branch)
- Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
