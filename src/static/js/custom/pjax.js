$(document).ready(function (){
    $(document).pjax('a', '#pjax-container');
    $(document).on('submit', 'form', function(event) {
        $.pjax.submit(event, "#pjax-container");
    });
    $(document).on('pjax:end', function() {
        $('#pjax-container').hide().slideDown(200);
    });
});
