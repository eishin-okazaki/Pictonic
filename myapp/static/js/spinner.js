document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll("form");
    const loadingOverlay = document.getElementById("loading-overlay");

    if(forms && loadingOverlay) {
        forms.forEach(function(form) {
            console.log(form);
            form.addEventListener("submit", function() {
                loadingOverlay.style.display = "flex";
            });
        });
    }
    
    if(loadingOverlay) {
        window.onload = function() {
            loadingOverlay.style.display = "none";
        };
    }
});