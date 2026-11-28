<?php
/* Saffra form handler: waitlist, questions, creator applications.
   Emails each submission to $TO and appends it to a CSV kept outside the public web folder. */
$TO   = '__NOTIFY_EMAIL__';          // where submissions are emailed
$FROM = 'no-reply@__DOMAIN__';       // must be an address on this site's own domain
$STORE = dirname(__DIR__, 2) . '/saffra-data';   // one level above the public folder

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
function out($ok, $msg = '', $code = 200) { http_response_code($code); echo json_encode(array('ok' => $ok, 'message' => $msg)); exit; }
function clean($v, $max) { $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', (string)$v)); return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max); }
function cell($v) { $v = str_replace(array("\r", "\n"), ' ', $v); return preg_match('/^[=+\-@\t]/', $v) ? "'" . $v : $v; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(false, 'Method not allowed.', 405);
if (!empty($_POST['website'])) out(true);                       // honeypot: bots fill this, people never see it
$kinds = array('waitlist' => 'Waitlist signup', 'ask' => 'Question', 'creator' => 'Creator application');
$kind = isset($_POST['kind']) ? (string)$_POST['kind'] : '';
if (!isset($kinds[$kind])) out(false, 'Unknown form.', 400);

if (!is_dir($STORE) && !@mkdir($STORE, 0700, true)) { $STORE = __DIR__ . '/data'; if (!is_dir($STORE)) @mkdir($STORE, 0700, true); @file_put_contents($STORE . '/.htaccess', "Require all denied\nDeny from all\n"); }

/* simple rate limit: 6 submissions per 10 minutes per visitor (address is hashed, never stored in the list) */
$ipkey = hash('sha256', (isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '') . '|saffra');
$rl = $STORE . '/rate-' . substr($ipkey, 0, 24) . '.txt'; $now = time();
$hits = array(); if (is_file($rl)) foreach (explode("\n", (string)@file_get_contents($rl)) as $t) if ((int)$t > $now - 600) $hits[] = (int)$t;
if (count($hits) >= 6) out(false, 'Too many tries. Please wait a few minutes.', 429);
$hits[] = $now; @file_put_contents($rl, implode("\n", $hits), LOCK_EX);

$fields = array(); $email = '';
foreach ($_POST as $k => $v) {
  if ($k === 'kind' || $k === 'website' || is_array($v)) continue;
  $k = preg_replace('/[^a-z0-9_-]/i', '', (string)$k); if ($k === '' || count($fields) >= 12) continue;
  $fields[$k] = clean($v, 2000);
}
foreach (array('email', 'askemail', 'cemail') as $ek) if (!empty($fields[$ek])) { $email = $fields[$ek]; break; }
if ($email !== '' && (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 254)) out(false, 'Enter a valid email address.', 400);
if ($kind === 'waitlist' && $email === '') out(false, 'Enter a valid email address.', 400);
if (!$fields) out(false, 'Nothing to send.', 400);

$row = array(gmdate('Y-m-d H:i:s') . ' UTC', $kind, $email);
foreach ($fields as $k => $v) $row[] = $k . ': ' . $v;
$fh = @fopen($STORE . '/' . $kind . '.csv', 'a');
$saved = false;
if ($fh) { if (flock($fh, LOCK_EX)) { $saved = fputcsv($fh, array_map('cell', $row)) !== false; flock($fh, LOCK_UN); } fclose($fh); }

$body = $kinds[$kind] . " from the Saffra site\n\n";
foreach ($fields as $k => $v) $body .= $k . ': ' . $v . "\n";
$body .= "\nReceived " . gmdate('Y-m-d H:i') . " UTC\n";
$headers = 'From: Saffra <' . $FROM . ">\r\nContent-Type: text/plain; charset=utf-8";
if ($email !== '') $headers .= "\r\nReply-To: " . $email;      // validated above, so it cannot carry extra headers
$mailed = filter_var($TO, FILTER_VALIDATE_EMAIL) ? @mail($TO, 'Saffra: ' . $kinds[$kind], $body, $headers) : false;

if (!$saved && !$mailed) out(false, 'We could not save that. Please try again.', 500);
out(true);
