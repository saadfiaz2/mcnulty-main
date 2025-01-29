'use strict';
{
    function setTheme(mode) {
        if (mode !== "light" && mode !== "dark") {
            console.error(`Got invalid theme mode: ${mode}. Resetting to light.`);
            mode = "light";
        }
        document.documentElement.dataset.theme = mode;
        localStorage.setItem("theme", mode);
    }

    function cycleTheme() {
        const currentTheme = localStorage.getItem("theme") || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

        // Toggle between light and dark
        if (currentTheme === "light") {
            setTheme("dark");
        } else {
            setTheme("light");
        }
    }

    function initTheme() {
        // Set theme based on localStorage or system preference
        const currentTheme = localStorage.getItem("theme");
        if (currentTheme) {
            setTheme(currentTheme);
        } else {
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
            setTheme(prefersDark ? "dark" : "light");
        }
    }

    window.addEventListener('load', function(_) {
        const buttons = document.getElementsByClassName("theme-toggle");
        Array.from(buttons).forEach((btn) => {
            btn.addEventListener("click", cycleTheme);
        });
    });

    initTheme();
}
