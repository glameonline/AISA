// Renders live reviews under each service. Usage: <div class="cf-reviews" data-service="studio"></div>
// services: studio, creator, social, build, search, growth. "all" shows every review.
(function () {
  var boxes = document.querySelectorAll('.cf-reviews'); if (!boxes.length) return;
  function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  function stars(n) { n = Math.round(n || 0); return '<span class="cf-stars" aria-label="' + n + ' out of 5 stars">' + '★★★★★'.slice(0, n) + '<span>' + '★★★★★'.slice(n) + '</span></span>'; }
  fetch('/reviews/reviews.php').then(function (r) { return r.json(); }).then(function (d) {
    boxes.forEach(function (box) {
      var svc = box.getAttribute('data-service');
      var list = d.reviews.filter(function (r) { return svc === 'all' || (r.services || []).indexOf(svc) > -1; })
                          .filter(function (r) { return (r.rating || 5) >= 4 && r.text; }).slice(0, 3);
      if (!list.length) return; // no real reviews for this service yet: show nothing
      var head = d.rating ? '<p class="cf-rev-head">' + stars(d.rating) + ' <strong>' + d.rating.toFixed(1) + '</strong> from ' + d.count + ' Google reviews' +
        (d.url ? ' · <a href="' + esc(d.url) + '" target="_blank" rel="noopener">See all on Google</a>' : '') + '</p>' : '';
      box.innerHTML = head + '<div class="cf-rev-list">' + list.map(function (r) {
        var who = r.author_url ? '<a href="' + esc(r.author_url) + '" target="_blank" rel="noopener nofollow">' + esc(r.author) + '</a>' : esc(r.author);
        return '<figure class="cf-rev">' + stars(r.rating) + '<blockquote>' + esc(r.text.length > 280 ? r.text.slice(0, 277) + '…' : r.text) +
          '</blockquote><figcaption>' + who + ' · ' + esc(r.when || r.date) + ' · ' + esc(r.source) + '</figcaption></figure>';
      }).join('') + '</div>';
      box.hidden = false;
    });
  }).catch(function () {});
})();
