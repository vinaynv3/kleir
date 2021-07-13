$(document).ready(function(){
  $(".fields").on('input', function(){

    var x = 0;
    var x = $("#num1").val();

    var y = 0;
    y = $("#num2").val();

    var z = parseFloat(x)+ parseFloat(y);
    if (isNaN(z)) z = 0;

    $("#total").val(z);
  });
});
