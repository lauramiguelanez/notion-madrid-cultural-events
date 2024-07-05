import { spawn } from "child_process";
import { join } from "path";
import { readdirSync } from "fs";

class EventScraper {
  constructor() {
    this.scriptsPath = "./scripts";
  }

  async runScript(path) {
    const pythonProcess = spawn("python", [path]);
    return new Promise((resolve, reject) => {
      pythonProcess.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
        resolve(data);
      });

      pythonProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
        reject(data);
      });

      pythonProcess.on("close", (code) => {
        console.log(`Python script exited with code ${code}`);
        // Perform further actions after Python script completes
      });
    });
  }

  async runPython(path) {
    try {
      await this.runScript(path);
    } catch (error) {
      console.error(`Error running ${path}: ${error.message}`);
    }
  }

  async runAllScripts() {
    const scriptFiles = readdirSync(this.scriptsPath);

    for (const file of scriptFiles) {
      const scriptPath = join(this.scriptsPath, file);
      await this.runPython(scriptPath);
    }
  }
}

export default new EventScraper();
