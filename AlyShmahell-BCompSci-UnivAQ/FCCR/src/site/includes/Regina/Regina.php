<?php 
namespace Regina;
class Regina
{
    public static function createTable($headArray,$bodyArray) {
        $tableStart = file_get_contents(__DIR__ . "/templates/table/tableStart.html");
        $tableEnd = file_get_contents(__DIR__ . "/templates/table/tableEnd.html");
        $rowStart = file_get_contents(__DIR__ . "/templates/table/rowStart.html");
        $rowEnd = file_get_contents(__DIR__ . "/templates/table/rowEnd.html");
        $columnTitle = file_get_contents(__DIR__ . "/templates/table/columnTitle.html");
        $cellData = file_get_contents(__DIR__ . "/templates/table/cellData.html");
    
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

    public static function createSelect($name,$valuesArray)
    {
     $select = file_get_contents(__DIR__ . "/templates/select/selectHeader.html");
     $select = str_replace("{{selectName}}",$name,$select);
     for($i = 0; $i<count($valuesArray); $i++)
       {
         $select = $select . file_get_contents(__DIR__ . "/templates/select/selectBody.html");
         $select = str_replace("{{optionValue}}",$valuesArray[$i],$select);
       }
     $select = $select . file_get_contents(__DIR__ . "/templates/select/selectFooter.html");
     return $select;
    }
}
