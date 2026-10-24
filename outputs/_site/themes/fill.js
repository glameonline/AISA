// Fills a theme demo with the chosen industry (from industries.js).
(function(){
  var d = IND[indKey()], r = document.documentElement.style;
  r.setProperty("--soft", d.c[0]); r.setProperty("--ac", d.c[1]); r.setProperty("--ink", d.c[2]);
  document.title = d.b + " · " + document.title;
  var set = function(sel, v){ document.querySelectorAll(sel).forEach(function(e){ e.textContent = v; }); };
  set(".brand", d.b); set(".tag", d.t); set(".ind", d.n); set(".ctat", d.cta); set("#em", d.e);
  var art = document.getElementById("art"); if (art) art.textContent = d.e;
  var blurbs = ["Done properly, first time.", "Clear prices before we start.", "Friendly local team.", "Fast, reliable and fully insured."];
  var svc = document.getElementById("svc");
  if (svc) svc.innerHTML = d.s.map(function(s, i){
    return '<div class="card reveal"><i>' + (i + 1) + '</i><h3>' + s + '</h3><p>' + blurbs[i % 4] + '</p></div>';
  }).join("");
  document.querySelectorAll(".call").forEach(function(a){ a.href = "tel:+44" + CALL.slice(1); });
})();
