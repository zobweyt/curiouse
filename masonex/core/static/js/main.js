$(document).ready(function() {    
    function initDefaultFormValues(form) {
        Array.from(form).forEach(el => el.dataset.defaultValue = el.value);
    }
    
    function isFormChanged(form) {
        return Array.from(form).some(el => 'defaultValue' in el.dataset && el.dataset.defaultValue !== el.value);
    }

    // TODO: make additional functions for every event. (then try this.button to access submit button)
    document.querySelectorAll('.needs-validation').forEach(form => {
        initDefaultFormValues(form);
        let button = form.querySelector('button[type=submit]');

        form.addEventListener('input', function() {
            const isValid = isFormChanged(this) && $(this)[0].checkValidity();

            if (isValid) {
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
