function sendPersonalizedEmails() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Diwanshu");
  var data = sheet.getDataRange().getValues();

  // Your email template with placeholders
  var template = `
<p>Dear <b>{{NAME}}</b>,</p>

<p>Greetings from <b>IIT Jodhpur!</b></p>

<p>I hope this message finds you in great spirits.</p>

<p>
At IIT Jodhpur, we take pride in hosting <b>Sandstone Summit 5.0</b>, our business and managerial conclave that celebrates leadership, innovation, and vision.
The summit is scheduled to take place on <b>September 27th and 28th, 2025</b>. Much like the enduring sands of our city, the Summit has become a symbol of resilience and inspiration for our community.
</p>

<p>
This year we explore the theme: <b>Innovate Today, Influence Tomorrow: Reimagining the Tech Landscape for a Sustainable Future</b>.
We aim to highlight the fact that the ideas we shape and the solutions we create today will set the course for the future of our society.
This era is defined by rapid technological progress and pressing sustainability challenges. It is important we identify the value of innovation.
Our theme emphasizes responsibility, collaboration, and vision: ensuring that our innovations lead not only to progress, but also to meaningful, sustainable change.
The summit is set to bring together brilliant minds from across industries, academia, and entrepreneurship, shaping conversations that matter for the future.
</p>

<p><b>Discussions will be centered around these key sub-themes:</b></p>
<ul>
  <li><b>Ethical AI and Tech for Tomorrow</b> - Balancing innovation with responsibility to ensure long-term societal benefits</li>
  <li><b>Global Collaboration in Innovation</b> - Bridging borders for collective problem-solving</li>
  <li><b>Data for Good</b> - Using big data and analytics to address climate, health, and societal challenges</li>
  <li><b>Green Tech Frontiers</b> - Advancing eco-friendly technologies for a carbon-neutral future</li>
</ul>

<p>{{CHEESY}}</p>

<p>
Please feel free to contact us with any concerns you have. We request you to share your schedule to confirm your availability so we can provide you with the best possible experience.
You may also find attached the event brochure for further details and insights about Sandstone Summit 5.0.
</p>

<p>
Looking forward to welcoming you at <b>IIT Jodhpur</b> for <b>Sandstone Summit 5.0</b>.
</p>

<p>
Best regards,<br>
<b>Vandita Gupta</b><br>
Head - Sandstone Team<br>
Contact - +91 8595117390<br>
IIT Jodhpur
</p>
`; // keep your existing template here

  for (var i = 1; i < data.length; i++) {
    try {
      var rowNum = i + 1; // spreadsheet rows start at 1
      var email = data[i][0];
      var name = data[i][1];
      var company = data[i][2];
      var fileId = data[i][3]; 
      var cheesyPara = data[i][4];

      // Skip if email is empty
      if (!email || email.toString().trim() === "") {
        Logger.log("Skipping row " + rowNum + " as email is empty.");
        continue;
      }

      // Check required fields
      if (!name || !fileId || !cheesyPara) {
        throw new Error("Missing required field(s) at row " + rowNum);
      }

      cheesyPara = cheesyPara.replace(/\n/g, "<br>");

      // Replace placeholders
      var htmlBody = template
        .replace("{{NAME}}", name)
        .replace("{{COMPANY}}", company || "") // optional company
        .replace("{{CHEESY}}", cheesyPara);

      var options = {
        htmlBody: htmlBody,
        name: "Sandstone Summit IIT Jodhpur"
      };

      if (fileId) {
        var file = DriveApp.getFileById(fileId);
        options.attachments = [file.getAs(MimeType.PDF)];
      }

      GmailApp.sendEmail(
        email,
        "Invitation as Guest Speaker | IIT Jodhpur Sandstone Summit 5.0",
        "",
        options
      );
    } catch (err) {
      throw new Error("Error in row " + (i + 1) + ": " + err.message);
    }
  }
}
