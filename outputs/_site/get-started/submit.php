<?php
// Lead form handler: emails the lead and appends it to a CSV OUTSIDE public_html. Config: set $TO below.
$TO = 'contentfellow1@gmail.com';            // <-- confirm the inbox that should receive leads
$CSV = dirname($_SERVER['DOCUMENT_ROOT']) . '/cf-leads.csv';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /get-started/'); exit; }
if (!empty($_POST['company_url'])) { header('Location: /get-started/thanks/'); exit; }   // honeypot: bots
$f = function ($k, $n = 300) { return trim(mb_substr(strip_tags((string)($_POST[$k] ?? '')), 0, $n)); };
$email = filter_var($f('email'), FILTER_VALIDATE_EMAIL);
if (!$email || !$f('name') || ($_POST['consent'] ?? '') !== 'yes') { header('Location: /get-started/?error=1'); exit; }
$services = implode(', ', array_map('strip_tags', (array)($_POST['services'] ?? [])));
$row = [date('c'), $f('name'), $f('business'), $f('website'), $email, $f('phone'), $f('area'), $services, $f('budget'), $f('message', 1000), $f('source'), $_SERVER['REMOTE_ADDR'] ?? ''];
$new = !is_file($CSV); $fh = @fopen($CSV, 'a');
if ($fh) { if ($new) fputcsv($fh, ['time','name','business','website','email','phone','area','services','budget','message','source','ip']); fputcsv($fh, $row); fclose($fh); }
$body = "New free-check request\n\n" . implode("\n", array_map(fn($k, $v) => "$k: $v", ['Name','Business','Website','Email','Phone','Area','Services','Budget','Message','Source'], array_slice($row, 1, 10)));
@mail($TO, "New lead: {$row[2]} ({$services})", $body, "From: ContentFellow <no-reply@contentfellow.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8");
header('Location: /get-started/thanks/');
