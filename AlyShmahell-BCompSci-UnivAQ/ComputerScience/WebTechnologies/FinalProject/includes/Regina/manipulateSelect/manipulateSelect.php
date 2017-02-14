<?php
function createSelect($name,$valuesArray)
{
 $select = file_get_contents(__DIR__ . "/selectHeader.html");
 $select = str_replace("{{selectName}}",$name,$select);
 for($i = 0; $i<count($valuesArray); $i++)
   {
     $select = $select . file_get_contents(__DIR__ . "/selectBody.html");
     $select = str_replace("{{optionValue}}",$valuesArray[$i],$select);
   }
 $select = $select . file_get_contents(__DIR__ . "/selectFooter.html");
 return $select;
}
?>
