document.getElementById('submitBtn').addEventListener('click', function() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            alert("Backend says: " + data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Could not reach the backend.");
        });
});