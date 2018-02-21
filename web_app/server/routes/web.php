<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/book', function () {
  $results = DB::select("SELECT book.ID_BOOK, subfield.CONTENT FROM book JOIN field ON(book.ID_BOOK = field.ID_BOOK) JOIN subfield ON (field.ID_FIELD = subfield.ID_FIELD)
WHERE field.CODE = '200' AND subfield.code = 'a'", [1]);
  return $results;
});

Route::post('/info', function () {
  $_POST = array_merge($_POST, (array) json_decode(file_get_contents('php://input')));
  $id = $_POST['id'];


  $results = DB::select("SELECT field.CODE, field.FIRST_INDICATOR, field.SECOND_INDICATOR, subfield.CODE as 'SUBFIELD_CODE', subfield.CONTENT
    FROM subfield JOIN field USING(ID_FIELD) WHERE field.ID_BOOK = ".$id." ORDER BY field.CODE, subfield.CODE", [1]);
  return $results;
});

Route::post('/find', function () {
  $_POST = array_merge($_POST, (array) json_decode(file_get_contents('php://input')));
  $niz = $_POST['niz'];

  $nizKodova = array();
  foreach($niz as $searchRow){
    $resultsObj = new stdClass();
    $resultsObj->value = $searchRow->value;
    $resultsObj->code = $searchRow->search->code;
    $resultsObj->statement=$searchRow->statement;
    array_push($nizKodova, $resultsObj);
  }

  $pomocZaUpit = "SELECT book.ID_BOOK FROM book JOIN field ON (book.ID_BOOK = field.ID_BOOK) JOIN subfield ON (field.ID_FIELD = subfield.ID_FIELD) JOIN prefix ON (field.CODE = prefix.FIELD_CODE AND subfield.CODE = prefix.SUBFIELD_CODE) WHERE ";
  $pomocZaUpit = $pomocZaUpit."prefix.PREFIX_CODE = '".$nizKodova[0]->code."'";
  $pomocZaUpit = $pomocZaUpit." AND subfield.CONTENT = '".$nizKodova[0]->value."'";

  $idRezultati = DB::select($pomocZaUpit, [1]);

  for($i = 1; $i<count($nizKodova); $i++){
    $trenutniObj = $nizKodova[$i];

    $pomocZaUpit = "SELECT book.ID_BOOK FROM book JOIN field ON (book.ID_BOOK = field.ID_BOOK) JOIN subfield ON (field.ID_FIELD = subfield.ID_FIELD) JOIN prefix ON (field.CODE = prefix.FIELD_CODE AND subfield.CODE = prefix.SUBFIELD_CODE) WHERE ";
    $pomocZaUpit = $pomocZaUpit."prefix.PREFIX_CODE = '".$trenutniObj->code."'";
    $pomocZaUpit = $pomocZaUpit." AND subfield.CONTENT = '".$trenutniObj->value."'";

    $idTrenutni = DB::select($pomocZaUpit, [1]);

    $pronadjeni = array();
    if($trenutniObj->statement=='&'){
      for($x=0; $x<count($idTrenutni); $x++){
        for($y=0; $y<count($idRezultati); $y++){
          if($idTrenutni[$x]==$idRezultati[$y]){
            array_push($pronadjeni, $idTrenutni[$x]);
          }
        }
      }
      $idRezultati = $pronadjeni;
    }
    elseif($trenutniObj->statement=='|') {
      for($x=0; $x<count($idTrenutni); $x++){
        if(!in_array($idTrenutni[$x], $idRezultati)){
          array_push($idRezultati, $idTrenutni[$x]);
        }
      }
    }


  }


  $konacniQuery = "SELECT field.ID_BOOK, field.CODE, subfield.CODE as 'SUBFIELD_CODE', subfield.CONTENT FROM subfield JOIN field USING(ID_FIELD) WHERE ((field.CODE = '200' AND subfield.CODE = 'a') OR (field.CODE = '210' AND subfield.CODE = 'c') OR (field.CODE = '700' AND subfield.CODE = 'a') OR (field.CODE = '700' AND subfield.CODE = 'b')) AND  field.ID_BOOK IN (";
  $konacniQueryDrugiDeo = "";
  $boolPrviLOL = true;
   for($x=0; $x<count($idRezultati); $x++){
     if($boolPrviLOL){
       $konacniQueryDrugiDeo = $konacniQueryDrugiDeo.$idRezultati[$x]->ID_BOOK;
       $boolPrviLOL = false;
     }
     else{
       // return $konacniQuery;
       $konacniQueryDrugiDeo = $konacniQueryDrugiDeo.",".$idRezultati[$x]->ID_BOOK;
     }
   }
   $konacniQuery = $konacniQuery.$konacniQueryDrugiDeo.")";
   // return $konacniQuery;
  $konacniRezultat = DB::select($konacniQuery, [1]);

  return $konacniRezultat;

});

Route::get('/search', function () {
  $results = DB::select('select * from prefix_names', [1]);
  return $results;
});
