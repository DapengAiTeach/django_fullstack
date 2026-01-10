(() => {
    const storageKey = "theme";
    const toggle = document.querySelector("[data-theme-toggle]");
    const icon = document.querySelector("[data-theme-icon]");

    const getPreferredTheme = () => {
        const storedTheme = localStorage.getItem(storageKey);
        if (storedTheme) {
            return storedTheme;
        }
        return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    };

    const setTheme = (theme) => {
        document.documentElement.setAttribute("data-bs-theme", theme);
        if (icon) {
            icon.classList.toggle("fa-moon", theme === "light");
            icon.classList.toggle("fa-sun", theme === "dark");
        }
        if (toggle) {
            toggle.setAttribute("aria-label", theme === "dark" ? "切换到亮色主题" : "切换到暗黑主题");
        }
    };

    const handleSystemChange = (event) => {
        const storedTheme = localStorage.getItem(storageKey);
        if (!storedTheme) {
            setTheme(event.matches ? "dark" : "light");
        }
    };

    const initTheme = () => {
        setTheme(getPreferredTheme());
    };

    initTheme();

    if (toggle) {
        toggle.addEventListener("click", () => {
            const currentTheme = document.documentElement.getAttribute("data-bs-theme") || "light";
            const nextTheme = currentTheme === "dark" ? "light" : "dark";
            localStorage.setItem(storageKey, nextTheme);
            setTheme(nextTheme);
        });
    }

    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", handleSystemChange);
})();
