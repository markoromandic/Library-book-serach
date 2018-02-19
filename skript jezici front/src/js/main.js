var app = angular.module("myApp", ['ui.select', 'ngSanitize']);

app.controller("myCtrl", function($scope, $http) {
  'ngInject';



  var vm=this;
  vm.more = 'READ MORE';
  vm.searchArray = [];
  vm.searchArraySelected = [{
    statement: '&'
  }];


  var baseUrl = 'http://localhost:8000';

  $scope.showKnjiga = false;

  vm.izabrana  = {};
  vm.sporedna = [];

  $scope.searchResults=[
    // {naziv: 'Strasna knjiga', izdavac:'Lasta basta', ime:'Nemanja', prezime:'Granic'},
    // {naziv: 'Strasna knjiga 2', izdavac:'Lasta basta', ime:'Nemanja', prezime:'Granic'}
  ];

  $scope.filterByNaziv = function(knjiga) {
      return (!vm.chNaziv || knjiga.naziv.includes(vm.txNaziv))&&(!vm.chIzdavac || knjiga.izdavac.includes(vm.txIzdavac))
        &&(!vm.chImeAutora || knjiga.ime.includes(vm.txImeAutora))&&(!vm.chPrezimeAutora || knjiga.prezime.includes(vm.txPrezimeAutora));
  };

  $scope.loadChanges = function() {
    vm.postActualSearch(vm.searchArraySelected).then((res)=>{
      console.log(res);

      // let poslednjiID = res.data[0].ID_BOOK;
      // let counter = 1;
      // for(let i=1; i<res.data; i++){
      //   if(poslednjiID!=res.data[i].ID_BOOK){
      //     if(counter<4){
      //       while(counter<4){
      //         res.data.push({}, i-1);
      //         counter++;
      //       }
      //     } else{
      //       poslednjiID = res.data[i].ID_BOOK;
      //       counter=1;
      //     }
      //
      //   } else {
      //     counter++;
      //   }
      // }

      $scope.searchResults = [];
      for(let i = 0; i<res.data.length; i+=4){
        let trenutniObj = {};
        for(let j=0; j<4; j++){
          trenutniObj.id = res.data[i+j].ID_BOOK;
          if(res.data[i+j].CODE == '200' && res.data[i+j].SUBFIELD_CODE == 'a'){
            trenutniObj.naziv = res.data[i+j].CONTENT;
          }
          else if (res.data[i+j].CODE == '210' && res.data[i+j].SUBFIELD_CODE == 'c') {
            trenutniObj.izdavac = res.data[i+j].CONTENT;
          }
          else if (res.data[i+j].CODE == '700' && res.data[i+j].SUBFIELD_CODE == 'a') {
            trenutniObj.prezime = res.data[i+j].CONTENT;
          }
          else if (res.data[i+j].CODE == '700' && res.data[i+j].SUBFIELD_CODE == 'b') {
            trenutniObj.ime = res.data[i+j].CONTENT;
          }
        }

        $scope.searchResults.push(trenutniObj);
      }


    }).catch((err)=>{
      console.log(err);
    });

  }

  $scope.izabran = function(knjiga) {
    console.log(knjiga.naziv);

    vm.postGetInfoOneBook(knjiga.id).then((res)=>{
      console.log(res);
      let onTheSpot = res.data[0].CODE;
      let vrednost = res.data[0].CODE+' '+ res.data[0].FIRST_INDICATOR+ res.data[0].SECOND_INDICATOR +' '+'['+res.data[0].SUBFIELD_CODE+']'+res.data[0].CONTENT;
      for(let i=0; i<res.data.length; i++){
        if(onTheSpot==res.data[i].CODE){
          vrednost+='['+res.data[i].SUBFIELD_CODE+']'+res.data[i].CONTENT;
        } else{
          vm.sporedna.push({
            linija: vrednost
          });
          onTheSpot = res.data[i].CODE;
          vrednost = res.data[i].CODE+' '+ res.data[i].FIRST_INDICATOR+ res.data[i].SECOND_INDICATOR +' '+'['+res.data[i].SUBFIELD_CODE+']'+res.data[i].CONTENT;
        }
      }
    }).catch((err)=>{
      console.log(err);
    });

    vm.izabrana = knjiga;
    $('#selectedBox').collapse('show');
  }

  $scope.close = function(){
    $('#selectedBox').collapse('hide');
  }

  $scope.readMore = function(){
    if(vm.more=='READ MORE'){
      vm.more='READ LESS';
    } else {
      vm.more='READ MORE'
    }

    $scope.showKnjiga = !$scope.showKnjiga;
  }

  vm.getBooks = function () {
    return $http({
      method: 'GET',
      url: baseUrl + '/book'
    });
  };

  vm.getSearch = function () {
    return $http({
      method: 'GET',
      url: baseUrl + '/search'
    });
  };

  vm.postActualSearch = function(arrayInfo){
    return $http({
      method: 'POST',
      url: baseUrl +  '/find',
      data: {niz: arrayInfo}
    });
  };

  vm.postGetInfoOneBook = function(id){
    return $http({
      method: 'POST',
      url: baseUrl +  '/info',
      data: {id: id}
    });
  };



  vm.getBooks().then((res)=>{
    console.log(res);
  }).catch((err)=>{
    console.log(err)
  });

  vm.getSearch().then((res)=>{
    for(i = 0; i<res.data.length; i++){
      let search = {};
      search.name = res.data[i].PREFIX_NAME;
      search.code = res.data[i].PREFIX_CODE;
      vm.searchArray.push(search);
    }
  }).catch((err)=>{
    console.log(err)
  });

  $scope.addStatementAnd = function(index){
    vm.searchArraySelected.splice(index+1, 0, {statement:'&'});
  }

  $scope.addStatementOr = function(index){
    vm.searchArraySelected.splice(index+1, 0, {statement:'|'});
  }

  $scope.removeStatement = function(index){
    vm.searchArraySelected.splice(index, 1);
    if(vm.searchArraySelected.length<=0){
      vm.searchArraySelected = [{
        statement: '&'
      }];
    }
  }

});
