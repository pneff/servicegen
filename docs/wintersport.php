<?php
function getStations($locationsDom, $numStations, $x, $y) {
    $retval = array();
    $xp = new DOMXPath($locationsDom);
    
    $radius = 5000;
    while (count($retval) < $numStations && $radius < 200000) {
        $stations = getStationsInRadius($xp, $x, $y, $radius);
        $new = array_diff($stations, $retval);
        $retval = array_merge($retval, $new);
        $radius += 5000;
    }
    return array_slice($retval, 0, $numStations);
}

function getStationsInRadius($xp, $x, $y, $radius) {
    $start_x = $x - $radius;
    $end_x = $x + $radius;
    $start_y = $y - $radius;
    $end_y = $y + $radius;
    
    $query = "/resorts/resort[swiss_x > $start_x and swiss_x < $end_x][swiss_y > $start_y and swiss_y < $end_y]";
    $res = $xp->query($query);
    
    $retval = array();
    foreach ($res as $resultItem) {
        array_push($retval, $xp->query('station', $resultItem)->item(0)->nodeValue);
    }
    return $retval;
}
