export class TemplateCreation {
    public labelContent: string;
    public isVisible: boolean;
    public visibleCode: string;
    public constructor(theLabelContent: string) { this.labelContent = theLabelContent; }

    public checkIfVisible(reportDefinition: string) {
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
        let navigArray: string[];

        navigArray = this.labelContent.split(" ");
        groupNum = "";
        lastLetter = navigArray[navigArray.length - 1];
        if (this.labelContent.indexOf("group") > -1) {
            if (lastLetter.match(/[a-z]/i)) {
                groupNum = navigArray[navigArray.length - 2];
                this.labelContent = navigArray.slice(0, navigArray.length - 2).join(" ");
            } else {
                groupNum = navigArray[navigArray.length - 1];
                this.labelContent = navigArray.slice(0, navigArray.length - 1).join(" ");
                lastLetter = "";
            }
        } else {
            this.labelContent = navigArray.slice(0, navigArray.length - 1).join(" ");
        }
        tabIndex = -1;
        foundIndex = 0;
        while (tabIndex === -1) {
            foundIndex = foundIndex + 30 + reportDefinition.substring(foundIndex + 30)
                .toLowerCase().indexOf(this.labelContent);
            if (foundIndex === -1) { break; }
            tabIndex = foundIndex - 36;
            tabIndex = reportDefinition.substring(tabIndex, foundIndex).indexOf("\n");
            if (groupNum !== "" && tabIndex > -1) {
                tabIndex = foundIndex + 30;
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
                this.isVisible = true;
                foundIndex = foundIndex + visibleSection;
            } else {
                this.isVisible = false;
                foundIndex = foundIndex + hiddenSection;
            }

            visibleSection = reportDefinition.substring(foundIndex + 10).indexOf("Visible,");
            hiddenSection = reportDefinition.substring(foundIndex + 10).indexOf("Hidden,");
            if (visibleSection < hiddenSection) {
                endOfRange = visibleSection;
            } else {
                endOfRange = hiddenSection;
            }

            visibleCodeIndex = reportDefinition.substring(foundIndex, foundIndex + endOfRange)
                .indexOf("Visible:");
            if (visibleCodeIndex > -1) {
                visibleCode = reportDefinition.substring(foundIndex + visibleCodeIndex + 8,
                    foundIndex + endOfRange);
                visibleCodeArray = visibleCode.split("\n");
                visibleCode = visibleCodeArray.slice(0, visibleCodeArray.length - 2).join("\n");
                this.visibleCode = visibleCode;
            }
        }
    }
}
