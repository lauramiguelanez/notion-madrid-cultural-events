import axios from "axios";
import { Client, LogLevel } from "@notionhq/client";

/**
 * Represents a Notion integration for accessing and manipulating data in a Notion database.
 */
class Notion {
  /**
   * Constructs a new instance of the Notion class.
   */
  constructor() {
    this.notionToken = process.env.NOTION_TOKEN;
    this.notionIntegrationToken = process.env.NOTION_INTEGRATION_TOKEN;
    this.databaseId = "c063cfeda1af4238b692285c598c5828"; // Replace with the database ID from the URL

    // Initializing a client
    this.notion = new Client({
      auth: this.notionIntegrationToken,
      logLevel: LogLevel.DEBUG,
    });
  }

  /**
   * Queries the Notion database and retrieves all elements.
   * @returns {Promise<Object>} A promise that resolves to the queried page.
   */
  async query() {
    const myPage = await this.notion.databases.query({
      database_id: this.databaseId,
    });
    console.log(myPage);
    return myPage;
  }

  /**
   * Saves an event object as a Notion database item.
   * @param {Object} event - The event object to be saved.
   * @returns {Promise<Object>} A promise that resolves to the saved page.
   */
  async saveEvent(event) {
    const newPage = await this.notion.pages.create({
      parent: {
        database_id: this.databaseId,
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
        /* 
        State: {
          status: {
            status: event.state,
          },
        },
        Organizer: {
          relation: [
            {
              id: event.organizerId,
            },
          ],
        },
        
        */
        Url: {
          url: event.url,
        },
        ImgCover: {
          files: [
            {
              external: { url: event.imageUrl },
              name: event.name,
              type: "external",
            },
          ],
        },
        Type: {
          select: {
            name: event.type,
          },
        },
        Date: {
          date: {
            start: event.dates[0],
            end: event.dates[1],
          },
        },
        Tags: {
          multi_select: event.tags?.map((tag) => ({
            name: tag,
          })),
        },
        Price: {
          number: event.price,
        },
        Location: {
          url: event.locationUrl,
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

    return newPage;
  }
}

export default new Notion();
