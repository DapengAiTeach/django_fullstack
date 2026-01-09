(() => {
    const container = document.querySelector(".captcha-field");
    if (!container) {
        return;
    }

    const image = container.querySelector("img");
    const keyInput = container.querySelector('input[name="captcha_0"]');
    const refreshUrl = container.dataset.refreshUrl || "/captcha/refresh/";

    if (!image || !keyInput) {
        return;
    }

    const refreshCaptcha = async () => {
        try {
            const response = await fetch(refreshUrl, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            image.src = data.image_url;
            keyInput.value = data.key;
        } catch (error) {
            // Silent fail to avoid breaking form submit flow.
        }
    };

    image.addEventListener("click", refreshCaptcha);
})();
