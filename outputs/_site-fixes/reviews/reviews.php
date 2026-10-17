<?php
// ContentFellow live reviews: pulls Google reviews (Places API New) + reviews.manual.json, tags each by service, caches 6 hours.
// Config lives OUTSIDE public_html: /home/<cpanel-user>/cf-reviews-config.php  ->  <?php return ['key' => '...', 'place_id' => '...'];
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=900');
$cfgFile = dirname($_SERVER['DOCUMENT_ROOT']) . '/cf-reviews-config.php';
$cache = sys_get_temp_dir() . '/cf-reviews-cache.json';
if (is_file($cache) && time() - filemtime($cache) < 6 * 3600) { readfile($cache); exit; }

$out = ['rating' => null, 'count' => 0, 'url' => null, 'reviews' => []];
if (is_file($cfgFile)) {
  $cfg = include $cfgFile;
  $ctx = stream_context_create(['http' => ['timeout' => 8, 'header' =>
    "X-Goog-Api-Key: {$cfg['key']}\r\nX-Goog-FieldMask: rating,userRatingCount,googleMapsUri,reviews\r\n"]]);
  $raw = @file_get_contents('https://places.googleapis.com/v1/places/' . rawurlencode($cfg['place_id']) . '?languageCode=en', false, $ctx);
  $g = $raw ? json_decode($raw, true) : null;
  if ($g) {
    $out['rating'] = $g['rating'] ?? null; $out['count'] = $g['userRatingCount'] ?? 0; $out['url'] = $g['googleMapsUri'] ?? null;
    foreach ($g['reviews'] ?? [] as $r) {
      $out['reviews'][] = ['source' => 'Google', 'author' => $r['authorAttribution']['displayName'] ?? 'Google user',
        'author_url' => $r['authorAttribution']['uri'] ?? null, 'rating' => $r['rating'] ?? null,
        'text' => $r['originalText']['text'] ?? ($r['text']['text'] ?? ''), 'when' => $r['relativePublishTimeDescription'] ?? '',
        'date' => substr($r['publishTime'] ?? '', 0, 10)];
    }
  }
}
// Real reviews from other platforms (Trustpilot, Facebook, email with permission). Never invent entries.
$manual = __DIR__ . '/reviews.manual.json';
if (is_file($manual)) foreach (json_decode(file_get_contents($manual), true) ?: [] as $r) $out['reviews'][] = $r;

// Tag by service: explicit "service" wins, else keywords in the text.
$kw = ['studio' => '/shoot|photo|videograph|filming|filmed|camera/i', 'creator' => '/edit|reel|tiktok|short|podcast|motion/i',
       'social' => '/social|instagram|facebook|posting|followers/i', 'build' => '/website|web site|site |web design|hosting/i',
       'search' => '/seo|google|ranking|chatgpt|search/i', 'growth' => '/growth|whole team|everything|all in one|strategy/i'];
foreach ($out['reviews'] as &$r) {
  if (empty($r['services'])) { $r['services'] = [];
    if (!empty($r['service'])) $r['services'][] = $r['service'];
    foreach ($kw as $s => $re) if (preg_match($re, $r['text'] ?? '')) $r['services'][] = $s;
    $r['services'] = array_values(array_unique($r['services'])); }
}
unset($r);
$json = json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
@file_put_contents($cache, $json);
echo $json;
