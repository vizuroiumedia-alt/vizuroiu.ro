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
    MailApp.sendEmail({
      to: p['Email'],
      subject: 'Mulțumim pentru mesaj — Vizuroiu Media',
      body:
        'Bună, ' + (p['Nume'] || '') + '!\n\n' +
        'Am primit solicitarea ta și te contactăm în cel mai scurt timp.\n\n' +
        'Cu drag,\nEchipa Vizuroiu Media\nhttps://vizuroiu.ro'
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
