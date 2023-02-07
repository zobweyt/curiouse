$(document).ready(function() {
    $('.bs-searchbox').find('.form-control').attr('placeholder', 'Filter');
    
    const form = $('.needs-validation');

    form.on('change input', function() {
        let button = $(this).find('button[type=submit]');
        let fields = $(this).find('[required]').toArray();

        if (fields.some((field) => !field.value.trim().length)) {
            button.attr('disabled', true);
        } else {
            button.attr('disabled', false);
        }
    });

    form.submit(function() {
        var button = $(this).find('button[type=submit]');
        button.prop('disabled', true);

        if (!$(this)[0].checkValidity()) {
            $(this).addClass('was-validated');
            $(this).find('.form-control:invalid').filter(':first').focus();
            return false;
        }

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
            image.addClass('rounded-4 flex-fill');
            target.html(image);
        }

        changeImage(this, image);
    });
});
