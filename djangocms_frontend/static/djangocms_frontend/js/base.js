document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".djangocms-frontend[role='tablist']").forEach(function (tablist) {
        const tabs = Array.from(tablist.querySelectorAll("[role='tab']"));
        if (!tabs.length) return;

        const panelFor = tab => document.getElementById(tab.getAttribute("aria-controls"));
        const activate = function (selected) {
            tabs.forEach(function (tab) {
                const active = tab === selected;
                tab.classList.toggle("active", active);
                tab.setAttribute("aria-selected", String(active));
                tab.tabIndex = active ? 0 : -1;
                const panel = panelFor(tab);
                panel.classList.toggle("show", active);
                panel.classList.toggle("active", active);
                panel.hidden = !active;
            });
        };

        tabs.forEach(function (tab, index) {
            const hasErrors = Boolean(panelFor(tab).querySelector("div.errors, ul.errorlist"));
            tab.classList.toggle("error", hasErrors);
            tab.querySelector(".tab-error-label").hidden = !hasErrors;
            tab.addEventListener("click", function () { activate(tab); });
            tab.addEventListener("keydown", function (event) {
                let next;
                const rtl = getComputedStyle(tablist).direction === "rtl";
                switch (event.key) {
                    case "ArrowRight": next = index + (rtl ? -1 : 1); break;
                    case "ArrowLeft": next = index + (rtl ? 1 : -1); break;
                    case "Home": next = 0; break;
                    case "End": next = tabs.length - 1; break;
                    default: return;
                }
                event.preventDefault();
                const selected = tabs[(next + tabs.length) % tabs.length];
                activate(selected);
                selected.focus();
            });
        });
        activate(tabs.find(tab => tab.classList.contains("error")) || tabs[0]);
    });
});
