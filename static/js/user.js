
$(document).ready(function(){
    $("#update").hide();

    var urlParams = new URLSearchParams(window.location.search);
    if(urlParams.has('update')){
      $("#update").show();
      $("#user").hide();
    }

    $("body").on("click", "button", function(){
        if($(this).text() === 'Update')
        {
            $("#update").show();
            $("#user").hide();
        }
        else if($(this).text() === 'Cancel') {
            $("#user").show();
            $("#update").hide();
        }
    });
});
