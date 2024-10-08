$(document).ready(function() {
    $('.login_user_image').click(function(event) {
        event.stopPropagation();
        $('.menu').toggle();
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('.menu').length) {
            $('.menu').hide();
        }
    });
});