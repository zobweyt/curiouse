$(document).ready(function() {
    let tableOfContents = $("#tableOfContents");
    const headers = $(".article__body").find('h1, h2, h3, h4');

    if (!headers[0]) {
        tableOfContents.append("This article has no headers.");
        return;
    }

    headers.each(function() {
        const text = $(this).text();
        const id = escape(text.toLowerCase());
        $(this).attr('id', id)
        tableOfContents.append($("<li>").append($("<a>", {"href": "#" + id}).text(text)));
    });
});
