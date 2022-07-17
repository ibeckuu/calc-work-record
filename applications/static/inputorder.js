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
