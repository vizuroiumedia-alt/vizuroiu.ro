/* Consimțământ cookies — Vizuroiu
 * - nu încarcă nimic de la terți până la „Accept"
 * - Google Ads (gtag) se încarcă doar după accept și doar dacă GOOGLE_ADS_ID e real
 * - alegerea se ține în localStorage ('vz_consent' = 'granted' | 'denied')
 */
(function(){
  /* Completează cu ID-ul real din Google Ads (ex: AW-123456789). Cât timp conține XXXX, nu se încarcă nimic. */
  var GOOGLE_ADS_ID = 'AW-XXXXXXXXXX';
  var KEY = 'vz_consent';

  function read(){ try { return localStorage.getItem(KEY); } catch(e){ return null; } }
  function write(v){ try { localStorage.setItem(KEY, v); } catch(e){} }

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ dataLayer.push(arguments); };

  var loaded = false;
  function loadAds(){
    if (loaded || GOOGLE_ADS_ID.indexOf('XXXX') !== -1) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GOOGLE_ADS_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GOOGLE_ADS_ID);
  }

  /* Folosit de formularul de contact: trimite conversia doar cu consimțământ. */
  window.vzTrackConversion = function(label){
    if (read() === 'granted' && GOOGLE_ADS_ID.indexOf('XXXX') === -1 && label) {
      gtag('event', 'conversion', {'send_to': GOOGLE_ADS_ID + '/' + label});
    }
  };

  var css = '#vz-cookie{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:720px;margin:0 auto;'
    + 'background:var(--surface,#161922);color:var(--text,#F4F5F7);border:1px solid var(--border,#242837);border-radius:16px;'
    + 'padding:18px 20px;box-shadow:0 20px 60px -20px rgba(0,0,0,.7);font:400 .9rem/1.5 "Inter",system-ui,sans-serif}'
    + '#vz-cookie p{margin:0 0 14px;color:var(--muted,#9AA0B0)}'
    + '#vz-cookie p a{color:var(--text,#F4F5F7);text-decoration:underline}'
    + '#vz-cookie .vz-row{display:flex;gap:10px;flex-wrap:wrap}'
    + '#vz-cookie button{flex:1 1 140px;cursor:pointer;font:700 .9rem "Bricolage Grotesque",system-ui,sans-serif;'
    + 'padding:.7rem 1.1rem;border-radius:999px;border:1px solid var(--border,#242837);background:transparent;color:var(--text,#F4F5F7)}'
    + '#vz-cookie button:hover{border-color:var(--accent,#FF5436)}';

  function hideBanner(){
    var b = document.getElementById('vz-cookie');
    if (b) b.remove();
  }

  function choose(v){
    write(v);
    hideBanner();
    if (v === 'granted') loadAds();
  }

  function showBanner(){
    if (document.getElementById('vz-cookie')) return;
    if (!document.getElementById('vz-cookie-css')) {
      var st = document.createElement('style');
      st.id = 'vz-cookie-css';
      st.textContent = css;
      document.head.appendChild(st);
    }
    var b = document.createElement('div');
    b.id = 'vz-cookie';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Setări cookies');
    b.innerHTML = '<p>Folosim cookie-uri de măsurare și publicitate (Google Ads) doar cu acordul tău. '
      + 'Site-ul funcționează complet și fără ele. '
      + '<a href="confidentialitate.html#cookies">Detalii despre cookies</a>.</p>'
      + '<div class="vz-row"><button type="button" data-v="denied">Refuz</button>'
      + '<button type="button" data-v="granted">Accept</button></div>';
    b.addEventListener('click', function(e){
      var v = e.target && e.target.getAttribute && e.target.getAttribute('data-v');
      if (v) choose(v);
    });
    document.body.appendChild(b);
  }

  document.addEventListener('click', function(e){
    var t = e.target && e.target.closest && e.target.closest('[data-cookie-settings]');
    if (t) { e.preventDefault(); showBanner(); }
  });

  function init(){
    var c = read();
    if (c === 'granted') loadAds();
    else if (c !== 'denied') showBanner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
