<?php
function createTable($headArray,$bodyArray) {
    $tableStart = file_get_contents(__DIR__ . "/tableStart.html");
    $tableEnd = file_get_contents(__DIR__ . "/tableEnd.html");
    $rowStart = file_get_contents(__DIR__ . "/rowStart.html");
    $rowEnd = file_get_contents(__DIR__ . "/rowEnd.html");
    $columnTitle = file_get_contents(__DIR__ . "/columnTitle.html");
    $cellData = file_get_contents(__DIR__ . "/cellData.html");

    $table = $tableStart;
    $table = $table. $rowStart;
    for($i = 0; $i < count($headArray); $i++)
    {
        $table = $table. $columnTitle;
        $table = str_replace("{{value}}", $headArray[$i], $table);
    }
    $table = $table. $rowEnd;


    for($i = 0; $i < count($bodyArray);$i=$i+count($headArray))
    {
        $table = $table. $rowStart;
        for($j = $i; $j < $i + count($headArray); $j++)
        {
            $table = $table. $cellData;
            $table = str_replace("{{value}}", $bodyArray[$j], $table);
        }
        $table = $table. $rowEnd;
    }
    $table = $table. $tableEnd;
    return $table;
}
?>
