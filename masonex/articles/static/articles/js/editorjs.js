$(document).ready(function() {
    $('#id_title').keydown(function(event) {
        if (event.which == 13) {
            $(this.form).find('.ce-paragraph').filter(':first').focus();
            event.preventDefault();
         }
    });

    $('form').on('change input', function() {
        if ($(this).find('.ce-paragraph').html() == '') {
            $(this).find('button[type=submit]').attr('disabled', true);
        }
    });
});
