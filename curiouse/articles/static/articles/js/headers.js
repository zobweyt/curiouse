document.addEventListener("DOMContentLoaded", function() {
    let contents = document.getElementById("tableOfContents");
    const anchors = document.querySelector(".article__body").querySelectorAll("h1, h2, h3");

    anchors.forEach(anchor => {
        const text = anchor.textContent;
        const id = escape(text);

        anchor.setAttribute("id", id)

        let navigationItem = document.createElement("li");

        let anchorLink = document.createElement("a");
        anchorLink.href = `#${id}`;
        anchorLink.text = text;

        navigationItem.appendChild(anchorLink);
        contents.appendChild(navigationItem);
    });
});
