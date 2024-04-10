// Function to restrict users from accessing developer tools
window.addEventListener("keydown", function(event) {
    if (event.keyCode == 116) {
        // block F5 (Refresh)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.keyCode == 122) {
        // block F11 (Fullscreen)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.keyCode == 123) {
        // block F12 (DevTools)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.ctrlKey && event.shiftKey && event.keyCode == 73) {
        // block Strg+Shift+I (DevTools)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.ctrlKey && event.shiftKey && event.keyCode == 74) {
        // block Strg+Shift+J (Console)
        event.preventDefault();
        event.stopPropagation();
        return false;
    }
});
window.oncontextmenu = function(event) {
    // block right-click / context-menu
    event.preventDefault();
    event.stopPropagation();
    return false;
};

// Checks alarms
function checkAlarms() {
    eel.check_alarms();
    console.log("Checking alarms..."); // DEBUG; TO BE REMOVED AT FINAL PRODUCT
}

// Timers to update to check alarms and update time.\
// Triggers every second to update time.
setInterval(function() {
    document.dispatchEvent(new Event('updateTimeEvent'));
}, 1000);

// Periodically update time every 1 second
setInterval(checkAlarms, 1000);
