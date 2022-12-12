$(document).ready(function() {
    $('[rel="tooltip"]').tooltip();
    $('[data-bs-toggle="popover"]').popover();

    $('.needs-validation').on('change input', function() {
        $(this).find('button[type=submit]').attr('disabled', false);
    })

    $('.needs-validation').on('submit', function() {
        const button = $(this).find('button[type=submit]');
        button.prop('disabled', true);

        if (!$(this)[0].checkValidity()) {
            $(this).addClass('was-validated');
            $(this).find('.form-control:invalid').filter(':first').focus()
            return false;
        }

        const text = button.attr('on-validation-text');

        if (text != "") {
            button.html(text);
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
            image.addClass('rounded cover-image cursor-pointer');
            target.html(image);
        }

        changeImage(this, image);
    });

    $('.bs-searchbox').find('.form-control').addClass('form-control-sm');
    $('.bs-searchbox').find('.form-control').attr('placeholder', 'Filter');
    $('.bs-searchbox').addClass('mb-1');
});
