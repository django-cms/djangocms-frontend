document.addEventListener("DOMContentLoaded", function () {
    let first = true;
    const links = document.getElementsByClassName("nav-link");
    for(let element of links) {
        element.addEventListener('click', function (event) {
            event.preventDefault();
            let parent = this.parentElement.parentElement;
            if (parent.tagName === "UL") {
                parent = parent.parentElement;
            }
            for (let button of parent.getElementsByClassName("nav-link")) {
                button.classList.remove("active");
            }
            parent = parent.parentElement;
            this.classList.add("active");
            for (let tab of parent.getElementsByClassName("tab-pane")) {
                tab.classList.remove("show", "active")
            }
            document.getElementById(this.dataset.bsTarget.substring(1)).classList.add("show", "active");
        });
        // mark tabs with errors
        const target = document.getElementById(element.dataset.bsTarget.substring(1));
        if (target.querySelectorAll('div.errors, ul.errorlist').length > 0) {
            element.classList.add("error");
            if (first) {
                element.classList.add("active");
                document.getElementById(element.dataset.bsTarget.substring(1)).classList.add("show", "active");
                first = false;
            }
         }
    }
    // No error: open first
    if(first) {
        links[0].classList.add("active");
        document.getElementById(links[0].dataset.bsTarget.substring(1)).classList.add("show", "active");
    }
});
