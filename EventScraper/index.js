import { join } from "path";
import { readdirSync } from "fs";
import { runPython } from "../utils/runPython";

class EventScraper {
  constructor() {
    this.scriptsPath = "./scripts";
  }

  runPython(path) {
    try {
      runPython(path);
    } catch (error) {
      console.error(`Error running ${path}: ${error.message}`);
    }
  }

  runAllScripts() {
    const scriptFiles = readdirSync(this.scriptsPath);

    scriptFiles.forEach((file) => {
      const scriptPath = join(this.scriptsPath, file);
      this.runPython(scriptPath);
    });
  }
}

export default new EventScraper();
