$(document).ready(function() {
    $('.bs-searchbox').find('.form-control').attr('placeholder', 'Filter');
    
    const form = $('.needs-validation');
    const origForm = form.serialize();

    form.on('change input', function() {
        var button = $(this).find('button[type=submit]');
        let disabled = $(this).find('.ce-paragraph').toArray().every((x) => !$(x).text().length)
        console.log(disabled);

        if (disabled) {
            button.prop('disabled', true);
            $(this).addClass('was-validated');
            return false;
        }
        
        if (!$(this)[0].checkValidity()) {
            button.prop('disabled', true);
            $(this).addClass('was-validated');
            return false;
        }

        button.prop('disabled', form.serialize() == origForm);
    });

    // TODO: make another js file for this (article editor).
    $('#id_title').keydown(function(event) {
        if (event.which == 13) {
            $(this.form).find('.ce-paragraph').filter(':first').focus();
            event.preventDefault();
         }
    });

    // $('form').on('change input', function() {
    //     var button = $(this).find('button[type=submit]');
    //     button.prop('disabled', form.serialize() == origForm);
    // });

    form.submit(function() {
        var button = $(this).find('button[type=submit]');
        button.prop('disabled', true);
        const text = button.attr('on-validation-text');
        
        if (text != "" && text != undefined) {
            button.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span>' + text);
        }
    });

    function changeImage(input, image) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                image.attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('[data-toggle="image"]').change(function () {
        let target = $($(this).attr('data-target'));
        let image = $(target.find('img'));
        const tagName = image.prop('tagName');

        if (tagName == undefined || tagName.toLowerCase() != 'img') {
            image = $(document.createElement('img'));
            image.addClass('rounded-4 flex-fill img-darken');
            target.html(image);
        }

        changeImage(this, image);
    });
});
