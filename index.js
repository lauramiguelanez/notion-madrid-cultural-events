import eventScraper from "./EventScraper/index.js";

import dotenv from "dotenv";
import NotionEvents from "./NotionIntegration/NotionEvents.js";

dotenv.config();

// await eventScraper.runAllScripts();

const exampleEvent = {
  name: "Example Event",
  state: "Active",
  organizer: "Espacio Fundaci\u00f3n Telef\u00f3nica",
  url: "https://example.com",
  type: "Conference",
  dates: ["2022-10-01", "2022-10-03"],
  imageUrl:
    "https://espacio.fundaciontelefonica.com/wp-content/uploads/2023/02/mundos-virtuales-1-450x450-550x410.jpg",
  tags: ["Photo", "Architecture", "Techno"],
  price: 10,
  locationUrl: "https://example.com/location",
  description: "This is an example event.",
};

// await NotionEvents.getAllOrganizers();
// await NotionEvents.saveEvent(exampleEvent);
await NotionEvents.saveEventsToNotion();
