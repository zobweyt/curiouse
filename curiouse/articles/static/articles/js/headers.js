let contents = document.getElementById("tableOfContents");
const anchors = document.querySelector(".markdown").querySelectorAll("h1, h2");

anchors.forEach(anchor => {
    const text = anchor.textContent;
    const id = slugify(text, {lower: true, remove: /[0-9]/, strict: true});

    $(anchor).nextUntil("h2").add(anchor).wrapAll(`<div id=${id}></div>`);

    // anchor.setAttribute("id", id)

    let navItem = document.createElement("li");
    navItem.classList.add("nav-item");

    let link = document.createElement("a");
    link.classList.add("nav-link")
    link.href = `#${id}`;
    link.text = text;

    navItem.appendChild(link);
    contents.appendChild(navItem);
});
