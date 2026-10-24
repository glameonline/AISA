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
    return '<div class="card reveal"><div class="ci" data-img="'+(i+3)+'" data-w="640" data-h="420"></div><i>' + (i + 1) + '</i><h3>' + s + '</h3><p>' + blurbs[i % 4] + '</p></div>';
  }).join("");
  // second vivid colour: accent rotated round the colour wheel
  var hx=d.c[1].slice(1),rr=parseInt(hx.substr(0,2),16)/255,gg=parseInt(hx.substr(2,2),16)/255,bb=parseInt(hx.substr(4,2),16)/255,mx=Math.max(rr,gg,bb),mn=Math.min(rr,gg,bb),hh=0;
  if(mx!=mn){hh=mx==rr?(gg-bb)/(mx-mn):mx==gg?2+(bb-rr)/(mx-mn):4+(rr-gg)/(mx-mn)}hh=(hh*60+360)%360;
  r.setProperty("--ac2","hsl("+((hh+150)%360)+" 90% 60%)");r.setProperty("--ac3","hsl("+((hh+60)%360)+" 95% 62%)");
  document.querySelectorAll("[data-img]").forEach(function(el){var u=IMG(+el.dataset.img,+el.dataset.w||1200,+el.dataset.h||800);
    if(el.tagName=="IMG"){el.src=u;el.onerror=function(){el.style.visibility="hidden"}}else el.style.backgroundImage="url("+u+"),linear-gradient(135deg,var(--ac),var(--ac2))"});
  document.querySelectorAll(".call").forEach(function(a){ a.href = "tel:+44" + CALL.slice(1); });
})();
