document.addEventListener('DOMContentLoaded', function() {
    var flashMessageElement = document.getElementById('flash-message');
    if (flashMessageElement) {
        var flashMessage = flashMessageElement.textContent.trim();
        if (flashMessage) {
            alert(flashMessage);
        }
    }
});
