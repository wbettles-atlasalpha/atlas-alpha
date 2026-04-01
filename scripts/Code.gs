function doPost(e) {
 var data = JSON.parse(e.postData.contents);
 var sheetName = data.sheet_name || "Portfolio"; 
 var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
 
 if (!sheet) return ContentService.createTextOutput("Error: Sheet not found");

 if (sheetName === "Waitlist") {
 var timestamp = new Date().toISOString();
 sheet.appendRow([timestamp, data.email, data.source || "Website"]);
 return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Added to waitlist"})).setMimeType(ContentService.MimeType.JSON);
 }
 
 // PORTFOLIO LOGIC
 if (sheetName === "Portfolio") {
 // NEW: Handle DELETE commands
 if (data.action === "DELETE") {
 var values = sheet.getDataRange().getValues();
 for (var i = values.length - 1; i >= 0; i--) {
 if (values[i][1] === data.ticker && values[i][2] === data.target_action) {
 sheet.deleteRow(i + 1);
 return ContentService.createTextOutput("Deleted Row");
 }
 }
 return ContentService.createTextOutput("Row not found for deletion");
 }
 
 // Correcting appendRow to match: 
 // A=Date, B=Ticker, C=Action, D=Shares, E=Entry Price, F=Live Price(F), G=Total Deployed(F), 
 // H=Category, I=Confidence, J=Invalidation Level, K=P/L $(F), L=P/L %(F), M=Status
 // We only provide values for: A, B, C, D, E, H, I, J, M.
 // Columns F, G, K, L, N, O, P, Q, R, S are formulas.
 
 if (data.action === "SELL") {
    // SELL logic (Existing)
    var values = sheet.getDataRange().getValues();
    for (var i = values.length - 1; i >= 0; i--) {
        if (values[i][1] === data.ticker && values[i][12] === "OPEN") { // Column M (13th col)
            sheet.getRange(i + 1, 11).setValue(data.pl_usd);  // Column K
            sheet.getRange(i + 1, 12).setValue(data.pl_pct);  // Column L
            sheet.getRange(i + 1, 13).setValue("CLOSED");      // Column M
            break;
        }
    }
 } else {
    // BUY logic
    // A:Date, B:Ticker, C:Action, D:Shares, E:Price, F:(Formula), G:(Formula), H:Category, I:Confidence, J:Invalidation, K:(Formula), L:(Formula), M:Status
    sheet.appendRow([
        data.date,          // A
        data.ticker,        // B
        data.action,        // C
        data.shares,        // D
        data.price,         // E
        null,               // F (Formula column)
        null,               // G (Formula column)
        data.category,      // H
        data.confidence,    // I
        data.invalidation,  // J
        null,               // K (Formula column)
        null,               // L (Formula column)
        "OPEN"              // M
    ]);
 }
 } 
 
 return ContentService.createTextOutput("Success");
}
