import eventScraper from "./EventScraper/index.js";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import Notion from "./NotionIntegration/Notion.js";

dotenv.config();
Notion.query();

const exampleEvent = {
  name: "Example Event",
  state: "Active",
  organizerId: "13ac5d7b34ec4040bc588304d65f8587",
  url: "https://example.com",
  type: "Conference",
  dates: ["2022-10-01", "2022-10-03"],
  imageUrl:
    "https://espacio.fundaciontelefonica.com/wp-content/uploads/2023/02/mundos-virtuales-1-450x450-550x410.jpg",
  tags: ["Photo", "Architecture", "Techno"],
  price: 100,
  locationUrl: "https://example.com/location",
  description: "This is an example event.",
};
Notion.saveEvent(exampleEvent);

/* await eventScraper.runAllScripts();

const dataDir = path.join(__dirname, "data");

fs.readdir(dataDir, (err, files) => {
  if (err) {
    console.error("Error reading data directory:", err);
    return;
  }

  files.forEach((file) => {
    const filePath = path.join(dataDir, file);
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error("Error reading file:", filePath, err);
        return;
      }

      // Do something with the data
      console.log(data);
    });
  });
});
*/
