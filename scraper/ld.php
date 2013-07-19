<?php
require_once('/usr/share/php/simplehtmldom/simple_html_dom.php');

# output
$fp = fopen('ld.csv', 'w');

#http://www.linuxlinks.com/Distributions/
$url = 'ld.html';
$html = file_get_html($url);
$lds = $html->find('ul[type=DISC] li');
foreach ($lds as $ld_li) {
  $ld_a = $ld_li->find('b a');
  $row = array();
  foreach ($ld_a as $ld) {
    if (isset($ld->href)) {
      $href = $ld->href;
      $anchor = $ld->plaintext;
      $row[] = $href;
      $row[] = $anchor;
    }
  }
  $row[] = $ld_li->find('div', 0)->plaintext;
  #$twitter_url = get_twitter_url($href);
  fputcsv($fp, $row);
}
fclose($fp);

function get_twitter_url($url) {
  $html = file_get_html($url);
  $links = $html->find('a');
  foreach ($links as $link) {
    $href = $link->href;
    if (false !== strpos($href, 'twitter.com')) {
      print_r($href);
    }
  }
}

function guess_twitter_url($url, $name) {
  $base = 'http://twiter.com/';
  $name = strtolower(preg_replace('|[^\w]|', '', $name));
  $twitter_url = $base . $name;
  var_dump($twitter_url);
  if (status_ok($twitter_url)) {
    return $twitter_url;
  }
  else {
    #var_dump(parse_url($url));
  }
  
}

function status_ok($url) {
  $ok = false;
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
  curl_exec($ch);
  if(!curl_errno($ch)) {
    $status_code = intval(curl_getinfo($ch, CURLINFO_HTTP_CODE));
    if (200 == $status_code) {
      $ok = TRUE;
    }
  }
  curl_close($ch);
  return $ok;
}