var operatorIdArr = [];
window.addEventListener('load', function(){
  $.ajax({
    type: 'GET',
    url: '/api/v1/operator/?working__exact=true',
    success: function(data, statusText, jqXHR){
      operatorIdArr.length = 0;
      $('#selectOperator').empty();
      $.each(data, function(index, value){
        var selectOpr = '<option>' + value.operator_name + '</option>';
        $(selectOpr).appendTo('#selectOperator');
        operatorIdArr.push(value.id);
      })
    }
  })
})

var descriptionIdArr = [];
var description = document.getElementById('inputDescription');
description.oninput = handleDescription;
function handleDescription(e){
  $.ajax({
    type: 'GET',
    url: '/api/v1/item/?description__contains=' + e.target.value,
    success: function(data, statusText, jqXHR){
      descriptionIdArr.length = 0;
      $('#selectDescription').empty();
      $.each(data, function(index, value){
        var selectDesc = '<option>' + value.description + '</option>';
        $(selectDesc).appendTo('#selectDescription');
        descriptionIdArr.push(value.id);
      })
    }
  })
}
