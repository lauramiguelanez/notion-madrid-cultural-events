import axios from "axios";
import dotenv from "dotenv";

class Notion {
  constructor(databaseId) {
    this.notionToken = process.env.NOTION_TOKEN;
    this.notionIntegrationToken = process.env.NOTION_INTEGRATION_TOKEN;
    this.databaseId = databaseId;
  }
}

export default new Notion();
