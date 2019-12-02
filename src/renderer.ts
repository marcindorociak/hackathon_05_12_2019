// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import * as fs from "fs";

document.getElementById("convert").addEventListener("submit", (evt) => {
    // prevent default refresh functionality of forms
    evt.preventDefault();

    const contents = fs.readFileSync("ocrAnalysisOfReport/output/filename0_2.txt", "utf8");
    console.log(contents);
})