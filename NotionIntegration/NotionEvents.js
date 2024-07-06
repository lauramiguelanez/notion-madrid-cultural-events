import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import { Client, LogLevel } from "@notionhq/client";

/**
 * Represents a Notion integration for accessing and manipulating data in a Notion database.
 */
class NotionEvents {
  /**
   * Constructs a new instance of the Notion class.
   */
  constructor() {
    this.notionIntegrationToken = process.env.NOTION_INTEGRATION_TOKEN;
    this.eventDb = process.env.NOTION_EVENTS_DATABASE_ID;
    (this.organizerDb = process.env.NOTION_ORGANIZER_DATABASE_ID),
      // Initializing a client
      (this.notion = new Client({
        auth: this.notionIntegrationToken,
        logLevel: LogLevel.DEBUG,
      }));
  }

  async saveEventsToNotion() {
    await this.getAllOrganizers();
    await this.processEvents();
  }

  async processEvents() {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    const dataDir = path.join(__dirname, "../data");

    fs.readdir(dataDir, (err, files) => {
      if (err) {
        console.error("Error reading data directory:", err);
        return;
      }

      files.forEach((file) => {
        const filePath = path.join(dataDir, file);
        fs.readFile(filePath, "utf8", async (err, data) => {
          if (err) {
            console.error("Error reading file:", filePath, err);
            return;
          }

          const events = JSON.parse(data);

          for (const event of events) {
            await this.saveEvent(event);
          }
        });
      });
    });
  }

  getOrganizerId(organizerName) {
    const organizer = this.organizers.find(({ name }) => {
      return name === organizerName;
    });
    return organizer?.id;
  }

  processDates(event) {
    if (event.dates?.length) {
      event.dates = event.dates.map((date) => {
        const d = new Date(date);
        return d.toISOString();
      });
    }
    return event;
  }

  /**
   * Saves an event object as a Notion database item.
   * @param {Object} event - The event object to be saved.
   * @returns {Promise<Object>} A promise that resolves to the saved page.
   */
  async saveEvent(data) {
    const event = this.processDates(data);
    const organizerId = this.getOrganizerId(event.organizer);

    // before saving it check if an event with the same event.name already exists
    const existingEvent = await this.notion.databases.query({
      database_id: this.eventDb,
      filter: {
        property: "Name",
        title: {
          contains: event.name,
        },
      },
    });
    if (existingEvent.results.length > 0) {
      console.log("Event already exists:", event.name);
      return;
    }

    const eventName = event.name.substring(0, 100);

    await this.notion.pages.create({
      parent: {
        database_id: this.eventDb,
      },
      properties: {
        Name: {
          title: [
            {
              text: {
                content: event.name,
              },
            },
          ],
        },

        Organizer: {
          relation: [
            {
              id: organizerId,
            },
          ],
        },

        ImgCover: {
          files: [
            {
              external: { url: event.image },
              name: eventName,
              type: "external",
            },
          ],
        },
        Url: {
          url: event.url,
        },
        Type: {
          select: {
            name: event.type,
          },
        },
        Date: event.dates.length
          ? {
              date: {
                start: event.dates[0],
                end: event.dates[1] || event.dates[0],
              },
            }
          : undefined,
        /* 
      Tags: {
        multi_select: event.tags?.map((tag) => ({
        name: tag,
        })),
      },
      Location: {
        url: event.locationUrl,
      },
      */
        Price: {
          number: event.price,
        },
        Description: {
          rich_text: [
            {
              text: {
                content: event.description,
              },
            },
          ],
        },
      },
    });

    return;
  }

  /**
   * Retrieves all items from the Notion database.
   * @returns {Promise<Array>} A promise that resolves to an array of all items.
   */
  async getAllOrganizers() {
    const response = await this.notion.databases.query({
      database_id: this.organizerDb,
    });

    this.organizers = response.results.map((result) => {
      return {
        id: result.id,
        name: result.properties.Name.title[0].plain_text,
      };
    });

    return this.organizers;
  }
}

export default new NotionEvents();
