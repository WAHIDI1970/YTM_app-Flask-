document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById("toggle-darkmode");
    const body = document.body;

    toggle.addEventListener('click', () => {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            toggle.textContent = "🌗 Mode sombre";
        } else {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            toggle.textContent = "🌞 Mode clair";
        }
    });
});
