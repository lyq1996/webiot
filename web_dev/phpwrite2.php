<?php
function analyJson($json_str) {
    $json_str = str_replace('＼＼', '', $json_str);
    $out_arr = array();
    preg_match('/{.*}/', $json_str, $out_arr);
    if (!empty($out_arr)) {
    $result = json_decode($out_arr[0], TRUE);
    } else {
    return FALSE;
    }
    return $result;
    }
$stringData = file_get_contents("php://input");
if (analyJson($stringData)){
    $myFile = 'status.json';
    $fh = fopen($myFile, 'w') or die('can\'t open file');
    fwrite($fh, $stringData);
    fclose($fh);
}
else{
    echo "What are you want to do?";
} 
?>