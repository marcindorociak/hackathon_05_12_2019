// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
import * as fs from "fs";

document.getElementById("convert").addEventListener("submit", (evt) => {
    // prevent default refresh functionality of forms
    evt.preventDefault();
    const anFolder = "ocrAnalysisOfReport/output/";
    const reportDefinitionPath = "crystalFiles/reportDefinition.txt";

    let navigation: string;
    let navigArray: string[];
    let reportDefinition: string;
    let foundIndex: number;
    let lastLetter: string;
    let visibleSection: number;
    let hiddenSection: number;
    let endOfRange: number;
    let visibleCodeIndex: number;
    let visibleCode: string;
    let visibleCodeArray: string[];
    let tabIndex: number;
    let groupNum: string;

    const lastNum = +fs.readFileSync(anFolder + "lastNum.txt", "utf8");
    reportDefinition = fs.readFileSync(reportDefinitionPath, "utf8");

    for (let i = 1; i < lastNum + 1; i++) {
        navigation = fs.readFileSync(anFolder + "filename0_" + i + ".txt", "utf8").split("\n")[0];
        if (navigation.replace(/\s\s+/g, "") !== "") {
            navigArray = navigation.split(" ");
            groupNum = "";
            lastLetter = navigArray[navigArray.length - 1];
            if (navigation.indexOf("group") > -1) {
                if (lastLetter.match(/[a-z]/i)) {
                    groupNum = navigArray[navigArray.length - 2];
                    navigation = navigArray.slice(0, navigArray.length - 2).join(" ");
                } else {
                    groupNum = navigArray[navigArray.length - 1];
                    navigation = navigArray.slice(0, navigArray.length - 1).join(" ");
                    lastLetter = "";
                }
            } else {
                navigation = navigArray.slice(0, navigArray.length - 1).join(" ");
            }
            tabIndex = -1;
            foundIndex = 0;
            console.log(navigation);
            while (tabIndex === -1) {
                foundIndex = foundIndex + reportDefinition.substring(foundIndex)
                                                            .toLowerCase().indexOf(navigation);
                if (foundIndex === -1) { break; }
                tabIndex = foundIndex - 6;
                tabIndex = reportDefinition.substring(tabIndex, foundIndex).indexOf("\n");
                if (groupNum !== "" && tabIndex > -1) {
                    tabIndex = foundIndex + 30;
                    console.log(tabIndex);
                    console.log(groupNum);
                    console.log(reportDefinition.substring(foundIndex, tabIndex));
                    tabIndex = reportDefinition.substring(foundIndex, tabIndex).indexOf(groupNum);
                }
            }
            if (foundIndex > -1 && (lastLetter.match(/[a-z]/i) || groupNum !== "")) {
                if (lastLetter.match(/[a-z]/i)) {
                    lastLetter = (lastLetter.charCodeAt(0) - 96).toString();
                    foundIndex = foundIndex + reportDefinition.substring(foundIndex)
                                                                .indexOf("Subsection." + lastLetter);
                }
                visibleSection = reportDefinition.substring(foundIndex).indexOf("Visible");
                hiddenSection = reportDefinition.substring(foundIndex).indexOf("Hidden");
                if (visibleSection < hiddenSection) {
                    console.log("Visible" + i);
                    foundIndex = foundIndex + visibleSection;
                } else {
                    console.log("Hidden" + i);
                    foundIndex = foundIndex + hiddenSection;
                }

                visibleSection = reportDefinition.substring(foundIndex).indexOf("Visible,");
                hiddenSection = reportDefinition.substring(foundIndex).indexOf("Hidden,");
                if (visibleSection < hiddenSection) {
                    endOfRange = visibleSection;
                } else {
                    endOfRange =  hiddenSection;
                }

                visibleCodeIndex = reportDefinition.substring(foundIndex, foundIndex + endOfRange)
                                                    .indexOf("Visible:");
                if (visibleCodeIndex > -1) {
                    visibleCode = reportDefinition.substring(foundIndex + visibleCodeIndex + 8,
                                                                foundIndex + endOfRange);
                    visibleCodeArray = visibleCode.split("\n");
                    visibleCode = visibleCodeArray.slice(0, visibleCodeArray.length - 2).join("\n");
                    console.log(visibleCode);
                }
            }
        }
        if (i === 8) { break; }
    }
});
