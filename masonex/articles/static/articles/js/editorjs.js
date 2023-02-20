document.addEventListener("DOMContentLoaded", function() {
    new TomSelect('[data-bs-toggle="tom-select"]', {
        maxItems: 3,
        plugins: {
            remove_button: {
                label: '',
                className: 'text-decoration-none ti ti-x ms-1'
            }
        },
        itemClass: 'badge bg-primary-lt m-0 py-1 ps-2 pe-1 me-1 d-flex align-items-center',
    });

    document.querySelector(".form-control-plaintext.h1").addEventListener("keydown", function(event) {
        if (event.which == 13) {
            this.form.querySelector('.ce-paragraph').focus();
            event.preventDefault();
        }
    });
});
