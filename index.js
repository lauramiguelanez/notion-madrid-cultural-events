import eventScraper from "./EventScraper/index.js";

import dotenv from "dotenv";
import NotionEvents from "./NotionIntegration/NotionEvents.js";

dotenv.config();

await eventScraper.runAllScripts();
// await NotionEvents.saveEventsToNotion();
