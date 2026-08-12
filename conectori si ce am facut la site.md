# Conectori și ce am făcut la site — Vizuroiu

_Ultima actualizare: 6 august 2026_

## Site-ul

- **Domeniul live**: `vizuroiu.ro` (nu `vizuroiumedia.net` — ăla e alt site Netlify, neconectat, cu subpagini care dau 404).
- Repo: GitHub `vizuroiumedia-alt/vizuroiu.ro`, auto-deploy prin Netlify la fiecare push pe `main`.
- Local: `/Users/admin/Documents/vizuroiumedia.net/site /claude code vsc/`

## Formularul de contact (`contact.html`)

- Trimite datele prin `fetch(mode:'no-cors')` către un Google Apps Script (NU printr-un POST clasic de formular — Apps Script blochează redirect-ul din sandbox și utilizatorul rămânea blocat pe o pagină goală script.google.com).
- Backend-ul: `google-apps-script/contact-form.gs`, deployat ca Web App, legat de un Google Sheet care ține toate submisiile (coloane: Data, Nume, Telefon, Email, Serviciu, Activitate afacere, Numele firmei).

## Conectorul Brevo (CRM + trimitere email)

**De ce**: ca fiecare submisie de formular să creeze automat un contact în baza de date Brevo, și ca emailurile trimise clienților să ajungă în Inbox, nu în Spam.

### Ce s-a configurat în Brevo (app.brevo.com)
- **Domeniu autentificat**: `vizuroiu.ro` — SPF, DKIM și DMARC toate verificate ✅
- **Subdomeniu branded** pentru linkuri: `mail.vizuroiu.ro`
- **Sender verificat**: `Vizuroiu <contact@vizuroiu.ro>`
- **API Key** generată (SMTP & API → API Keys) — **nu e stocată în cod/repo**, ci în Apps Script → Project Settings → Script Properties, sub numele `BREVO_API_KEY`.

### Ce face codul (`contact-form.gs`)
La fiecare submisie de formular (`doPost`):
1. Scrie rândul în Google Sheet (ca înainte).
2. **`createBrevoContact_`** — trimite emailul + numele + telefonul către Brevo Contacts API (`POST /v3/contacts`), ca să apară contactul în Brevo.
3. **`sendBrevoConfirmationEmail_`** — trimite emailul de confirmare către client prin Brevo Transactional Email API (`POST /v3/smtp/email`), de pe `contact@vizuroiu.ro`, cu **Reply-To** setat spre `vizuroiumedia@gmail.com` (ca răspunsurile clienților să ajungă tot pe Gmail-ul folosit până acum, fără mailbox nou).
4. Dacă Brevo pică din orice motiv (cheie lipsă, eroare API), codul **cade automat pe `MailApp`** (Gmail-ul contului care rulează scriptul) ca fallback, deci site-ul nu rămâne fără notificări.
5. Emailul intern de notificare (către `vizuroiumedia@gmail.com`, cu datele completate de client) conține acum și un bloc **"Brevo status"** la final, cu rezultatul exact (OK sau eroare) al pașilor 2 și 3 — adăugat special ca să fie ușor de depanat fără să mai umblăm prin Apps Script → Executions.

### Probleme întâlnite și rezolvate pe parcurs
- Un **trigger** greșit configurat pe `doPost` (declanșat "On open" / "From spreadsheet") producea erori la fiecare deschidere a Sheet-ului — a fost șters.
- Interfața Apps Script → Executions nu se deschidea ușor pentru execuțiile de tip "Web App" — de aceea am mutat diagnosticul direct în emailul de notificare (mai simplu de verificat).

### Status curent — NEFINALIZAT
Ultimul test a arătat emailul de confirmare venind tot de pe `vizuroiumedia@gmail.com` (deci încă pe fallback, nu prin Brevo). **Nu s-a confirmat încă** dacă integrarea Brevo funcționează corect.

**Următorul pas** (de reluat): deschide emailul cu subiectul **"Mesaj nou de pe site — Vizuroiu"** primit la ultimul test și verifică blocul "Brevo status" de la final — acolo scrie exact ce a răspuns Brevo (succes sau eroare). În funcție de eroare, se corectează (cheie API greșit lipită, atribute lipsă în Brevo, etc.).

## Idei / de făcut mai departe
- Odată ce Brevo merge, se poate trece la campanii/segmentare pe baza contactelor colectate din formular.
- De verificat dacă atributele custom (`NUME`, `TELEFON`) există în Brevo → Contacts → Settings → Contact attributes (dacă nu există, API-ul poate refuza crearea contactului).
- De luat în calcul, pe termen lung, o căsuță email reală `contact@vizuroiu.ro` (Google Workspace sau forwarding) dacă volumul de răspunsuri crește.
