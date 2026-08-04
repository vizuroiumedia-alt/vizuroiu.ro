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
      subject: 'Mulțumim pentru mesaj — Vizuroiu Media',
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
    subject: 'Mesaj nou de pe site — Vizuroiu Media',
    body:
      'Nume: ' + (p['Nume'] || '') + '\n' +
      'Telefon: ' + (p['Telefon'] || '') + '\n' +
      'Email: ' + (p['Email'] || '') + '\n' +
      'Serviciu: ' + (p['Serviciu'] || '') + '\n' +
      'Activitate afacere: ' + (p['Activitate afacere'] || '') + '\n' +
      'Numele firmei: ' + (p['Numele firmei'] || '') + '\n' +
      'CUI: ' + (p['CUI'] || '')
  });

  return HtmlService.createHtmlOutput(
    '<script>window.top.location.href="https://vizuroiu.ro/contact.html?trimis=1";</script>'
  );
}

function buildConfirmationEmailHtml_(nume) {
  var logoBase64 = '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';
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
                <td style="vertical-align:middle; padding-right:10px;">
                  <img src="data:image/png;base64,${logoBase64}" alt="Vizuroiu" width="32" style="display:block; border:0;">
                </td>
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
