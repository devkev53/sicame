$(document).ready(function(){
    $('form').submit(function() {
        var c = confirm("continue submitting ?");
        return c;
    });
})