$(document).ready(function() {
    document.querySelectorAll('input[type=email]').forEach(input => {
        input.setAttribute('pattern', "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$");
    });
    
    // TODO: make additional functions for every event. (then try this.button to access submit button)
    document.querySelectorAll('.needs-validation').forEach(form => {
        let button = form.querySelector('button[type=submit]');
        button.setAttribute('disabled', true);

        form.addEventListener('input', function() {
            if (form.checkValidity()) {
                button.removeAttribute('disabled');
            } else {
                button.setAttribute('disabled', true);
            }
        });

        form.addEventListener('submit', function() {
            button.setAttribute('disabled', true);         
            let icon = button.querySelector('.icon');

            if (icon) {
                icon.remove();
            }

            let spinner = document.createElement('span');
            spinner.classList.add('spinner-border', 'spinner-border-sm', 'me-2');
            spinner.setAttribute('role', 'status');

            button.insertBefore(spinner, button.firstChild);
        });
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

    $('[data-toggle="image"]').change(function() {
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
