
  $(function(){
    $.ajax("/api/status")
    .done(function( data ) {
      for(datum of data){
        let newOption = $('<option>');
        newOption.val(datum).text(datum);
        $('#status').append(newOption);
      }
      $('#status').addClass('green');
      setTimeout(() => {
        $('#status').removeClass('green')
      }, 3000);
    });
  });

  let checkApi = function(){
    $.ajax("/api/")
    .done(function( data ) {
      $('#result').text(JSON.stringify(data));
      if (data.status === 'ok'){
        $('#result').addClass('green').removeClass('red');
      }else if (data.status === 'nok'){
        $('#result').addClass('red').removeClass('green');
      }
      setTimeout(() => {
        $('#result').removeClass('red').removeClass('green')
      }, 3000);
    });
  }
  $('#clickMe').on('click', checkApi);