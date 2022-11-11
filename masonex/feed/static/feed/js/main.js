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

    function changeAvatar(input, image) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                image.attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('[data-toggle="change-avatar"]').change(function () {
        changeAvatar(this, $($(this).attr('data-target')).find('img'));
    });

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
    
    const responsiveTabs = $('.responsive-tabs');
    
    responsiveTabs.find('[role="tablist"]').addClass('d-md-block');
    responsiveTabs.find('[role="tablist-header"]').addClass('d-block d-md-none');
    responsiveTabs.find('[role="contentlist"]').addClass('d-none d-md-block');
    
    responsiveTabs.find('.tab-pane').prepend(`
    <button class="btn-back d-block d-md-none rounded" data-toggle="close-tab">
        <svg xmlns="http://www.w3.org/2000/svg" class="me-1" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <line x1="5" y1="12" x2="11" y2="18"></line>
            <line x1="5" y1="12" x2="11" y2="6"></line>
        </svg>
        <span>Back</span>
    </button>`);

    responsiveTabs.find('[data-toggle="close-tab"]').on('click', function() {
        const tablist = $('#' + $(this).parent().attr('aria-labelledby')).closest('[role="tablist"]');
        $(this).closest('[role="contentlist"]').addClass('d-none');
        tablist.removeClass('d-none');
        const header = tablist.parent().find('[role="tablist-header"]');
        header.html(header.attr('default-title'));
    });

    responsiveTabs.find('[role="tab"]').on('click', function() {
        $(this).closest('[role="tablist"]').addClass('d-none');
        $('#' + $(this).attr('aria-controls')).closest('.tab-content').removeClass('d-none');
        $('[role="tablist-header"]').html($(this).html());
    });

    $('.dropdown-toggle').on('show.bs.dropdown', function() {
        $(this).find('.dropdown-chevron').addClass('flip');
    });

    $('.dropdown-toggle').on('hide.bs.dropdown', function() {
        $(this).find('.dropdown-chevron').removeClass('flip');
    });
});
