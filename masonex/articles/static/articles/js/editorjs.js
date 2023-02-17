document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".needs-validation");
    let submit = form.querySelector("button[type=submit]");

    form.querySelector(".form-control-plaintext").addEventListener("keydown", function(event) {
        if (event.which == 13) {
            this.form.querySelector('.ce-paragraph').focus();
            event.preventDefault();
        }
    });

    form.addEventListener("input", function() {
        if (this.querySelector('.ce-paragraph').textContent == '') {
            submit.setAttribute('disabled', true);
        }
    });
});
