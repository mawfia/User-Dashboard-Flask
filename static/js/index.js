
$(document).ready(function(){
    $("#register").hide();
    $("#login").hide();

  /*  var urlParams = new URLSearchParams(window.location.search);
    if(urlParams.has('create')){
      //$("#update").hide();
      //$("#user").hide();
      $("#create").show();
      $("button:nth-of-type(1)").hide();
      $("button:nth-of-type(2)").hide();
    }*/

    if( $('span').text() == 1){
      $("#create").show();
      $("#select").hide();
      $("button:nth-of-type(1)").hide();
      $("button:nth-of-type(2)").hide();
    }

    $("#select").on("click", "button", function(){
        if($(this).text() === 'Register')
        {
            $("#register").show();
            $("#login").hide();
            $("button:nth-of-type(2)").hide();
            $("button:nth-of-type(1)").show();
        }
        else if($(this).text() === 'Login') {
            $("#login").show();
            $("#register").hide();
            $("button:nth-of-type(1)").hide();
            $("button:nth-of-type(2)").show();
        }
    });
});
