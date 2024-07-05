import { spawn } from "child_process";

export const runPython = (scriptPath) => {
  const pythonProcess = spawn("python", [scriptPath]);
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
};
