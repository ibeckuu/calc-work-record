var operatorIdArr = [];
var selectOperator = document.getElementById('selectOperator');
selectOperator.onfocus = handleSelect;
function handleSelect(e){
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
}

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
