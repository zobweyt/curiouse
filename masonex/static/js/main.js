$(document).ready(function() {
    $('[rel="tooltip"]').tooltip();
    $('[rel="tooltip').on('click', function() {
        $(this).tooltip('hide');
    });

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

    const scrollToTop = $('#scroll-to-top');
    scrollToTop.hide();
    scrollToTop.css("transform", "translateY(75px)");
    var previousScrollPosition = $(window).scrollTop();
 
    $(window).scroll(function() {
        var currentScrollPosition = $(window).scrollTop();
        if (currentScrollPosition < 400) {
            scrollToTop.css("transform", "translateY(75px)");
        } 
        else if (currentScrollPosition > previousScrollPosition) {
            scrollToTop.css("transform", "translateY(75px)");
            scrollToTop.show();
        } else {
            scrollToTop.css("transform", "none");
        }
        previousScrollPosition = currentScrollPosition;
    });

    scrollToTop.on('click', function() {
        window.scroll({
            top: 0,
            left: 0,
        });
    });

    scrollToTop.mouseover(function(){
        if (previousScrollPosition > 400) {
            scrollToTop.css("transform", "translateY(-5px)");
        } 
    }).mouseleave(function(){
        if (previousScrollPosition > 400) {
            scrollToTop.css("transform", "none");
        } 
    });

    $('.dropdown-toggle').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-chevron').addClass('flip');
    });

    $('.dropdown-toggle').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-chevron').removeClass('flip');
    });

    $('[data-bs-toggle="popover"]').popover();
});
