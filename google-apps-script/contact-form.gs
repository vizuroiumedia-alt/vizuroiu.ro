/**
 * Script pentru Google Sheets (Extensions → Apps Script), legat de un Sheet
 * care primește submisiile din formularul de contact al site-ului.
 *
 * Deploy: Deploy → New deployment → Web app → Execute as: Me →
 * Who has access: Anyone → Deploy. URL-ul rezultat se pune ca "action"
 * în formularul din contact.html.
 */

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Data', 'Nume', 'Telefon', 'Email', 'Serviciu', 'Activitate afacere', 'Numele firmei', 'CUI']);
  }

  var p = e.parameter;
  sheet.appendRow([
    new Date(),
    p['Nume'] || '',
    p['Telefon'] || '',
    p['Email'] || '',
    p['Serviciu'] || '',
    p['Activitate afacere'] || '',
    p['Numele firmei'] || '',
    p['CUI'] || ''
  ]);

  if (p['Email']) {
    var nume = p['Nume'] || 'Client';
    MailApp.sendEmail({
      to: p['Email'],
      subject: 'Mulțumim pentru mesaj — Vizuroiu',
      body:
        'Mulțumim, ' + nume + '!\n\n' +
        'Am primit datele tale și confirmăm înscrierea. Echipa noastră de content marketing analizează ' +
        'informațiile transmise și te va contacta în cel mai scurt timp.\n\n' +
        'Echipa Vizuroiu',
      htmlBody: buildConfirmationEmailHtml_(nume)
    });
  }

  MailApp.sendEmail({
    to: 'vizuroiumedia@gmail.com',
    subject: 'Mesaj nou de pe site — Vizuroiu',
    body:
      'Nume: ' + (p['Nume'] || '') + '\n' +
      'Telefon: ' + (p['Telefon'] || '') + '\n' +
      'Email: ' + (p['Email'] || '') + '\n' +
      'Serviciu: ' + (p['Serviciu'] || '') + '\n' +
      'Activitate afacere: ' + (p['Activitate afacere'] || '') + '\n' +
      'Numele firmei: ' + (p['Numele firmei'] || '') + '\n' +
      'CUI: ' + (p['CUI'] || '')
  });

  // Formularul trimite prin fetch(mode:'no-cors') din contact.html, deci acest
  // răspuns nu e citit de browser — succesul e afișat direct în pagină.
  return ContentService.createTextOutput('OK');
}

function buildConfirmationEmailHtml_(nume) {
  var template = `<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Email confirmare formular</title>
</head>
<body style="margin:0; padding:0; background-color:#f5e6de; -webkit-text-size-adjust:100%; text-size-adjust:100%;">

<div style="display:none; max-height:0; overflow:hidden; mso-hide:all;">
  Mulțumim pentru completarea formularului — documentul tău este pregătit mai jos.
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0e4dc; padding:40px 0;">
  <tr>
    <td align="center">

      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:#182a35; background-image:linear-gradient(120deg, #dddddd 0%, #75787d 15%, #182a35 30%, #5a3218 45%, #b75a1c 60%, #ef721d 75%, #ff8a26 90%, #fd8622 100%); border-radius:14px; overflow:hidden; font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; max-width:600px; width:100%; box-shadow:0 4px 24px rgba(0,0,0,0.25);">

        <tr>
          <td style="background-color:#e8654f; height:4px; line-height:4px; font-size:0;">&nbsp;</td>
        </tr>

        <tr>
          <td style="padding:32px 44px 24px 44px;" align="left">
            <table role="presentation" cellpadding="0" cellspacing="0">
              <tr>
                <td style="vertical-align:middle;">
                  <span style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:20px; font-weight:800; letter-spacing:0.5px; color:#f5ece6; text-transform:uppercase;">Vizuroiu</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:0 44px;">
            <table role="presentation" cellpadding="0" cellspacing="0">
              <tr>
                <td style="background-color:#5a3218; border-radius:20px; padding:6px 14px;">
                  <span style="font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; font-size:12px; font-weight:bold; letter-spacing:0.5px; color:#f5ece6; text-transform:uppercase;">
                    ✓ Formular confirmat
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:24px 44px 8px 44px;">
            <h1 style="margin:0 0 16px 0; font-size:26px; line-height:1.35; color:#f5ece6; font-weight:700; letter-spacing:-0.3px;">
              Mulțumim, {{Nume}}!
            </h1>
            <p style="margin:0 0 18px 0; font-size:16px; line-height:1.65; color:#f5ece6;">
              Am primit datele tale și confirmăm înscrierea. Echipa noastră de content marketing analizează
              informațiile transmise și te va contacta în cel mai scurt timp.
            </p>
          </td>
        </tr>

        <tr>
          <td style="padding:32px 44px 0 44px;">
            <hr style="border:none; border-top:1px solid rgba(255,255,255,0.25); margin:0;">
          </td>
        </tr>

        <tr>
          <td style="padding:24px 44px 36px 44px;">
            <p style="margin:0; font-size:19px; font-style:italic; font-weight:600; color:#f5ece6; letter-spacing:0.3px; font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;">
              Echipa Vizuroiu
            </p>
          </td>
        </tr>

        <tr>
          <td style="background-color:rgba(0,0,0,0.15); padding:28px 44px; text-align:center; border-top:1px solid rgba(255,255,255,0.2);">
            <p style="margin:0 0 10px 0; font-size:12px; color:#f0e2d9;">
              Vizuroiu · Adresa companiei, Oraș, România
            </p>
            <p style="margin:0; font-size:12px; color:#f0e2d9;">
              <a href="#" style="color:#f0e2d9; text-decoration:underline;">Dezabonare</a>
              &nbsp;&middot;&nbsp;
              <a href="#" style="color:#f0e2d9; text-decoration:underline;">Politica de confidențialitate</a>
            </p>
          </td>
        </tr>

      </table>

      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%;">
        <tr>
          <td style="padding:20px 44px 0 44px; text-align:center;">
            <p style="margin:0; font-size:12px; color:#f2e8e2; font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;">
              © 2026 Vizuroiu. Toate drepturile rezervate.
            </p>
          </td>
        </tr>
      </table>

    </td>
  </tr>
</table>

</body>
</html>`;

  return template.replace(/{{Nume}}/g, nume);
}
