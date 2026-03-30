     // Wait for the page to load
 setTimeout(function() {
        let msg = document.getElementById("messages_container_inner");
        if (msg) {
            msg.style.transition = "opacity 1s";
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 1000); // Remove from DOM after fade
        }
    }, 2500);