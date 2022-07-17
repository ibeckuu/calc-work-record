
var customerIdArr = [];
var input = document.getElementById('inputCustomerName');
input.oninput = handleInput;
function handleInput(e) {
  $.ajax({
    type: 'GET',
    url: '/api/v1/customer/?name__contains=' + e.target.value + '&delete__exact=False',
    success: function (data, statusText, jqXHR) {
      customerIdArr.length = 0;
      $('#selectCustomer').empty();
      $.each(data, function (index, value) {
        var selectItem = '<option>' + value.customer_name + '</option>';
        $(selectItem).appendTo('#selectCustomer');
        customerIdArr.push(value.id);
      })
    }
  })
}

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
