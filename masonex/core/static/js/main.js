document.addEventListener("DOMContentLoaded", function() {
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

    function changeImage(input, image, target) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(event) {
                image.src = event.target.result;
                target.innerHTML = image.outerHTML;
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    document.querySelectorAll('[data-toggle="image"]').forEach(el => el.addEventListener("change", function() {
        let target = document.querySelector(this.getAttribute("data-target"));
        let image = target.querySelector("img");
        const style = this.getAttribute("data-style");
        
        if (image?.tagName != "IMG") {
            image = document.createElement("img");
            if (style) {
                style.split(" ").forEach(cls => image.classList.add(cls));
            }
        }
        
        changeImage(this, image, target);
    }));
});
