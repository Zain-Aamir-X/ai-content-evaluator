document.getElementById('submitBtn').addEventListener('click', function() {
    const textInput = document.getElementById('textInput').value.trim();
    const fileInput = document.getElementById('fileInput').files[0];
    const resultsSection = document.getElementById('resultsSection');
    
    // 1. Validate input
    if (!textInput && !fileInput) {
        alert("Please paste some text or upload a file first.");
        return;
    }

    // 2. Prepare the data payload
    const formData = new FormData();
    if (fileInput) {
        formData.append('file', fileInput);
    } else {
        formData.append('text', textInput);
    }

    // 3. Show loading state
    const btn = document.getElementById('submitBtn');
    btn.innerHTML = 'Processing...';
    btn.disabled = true;

    // 4. Send to backend
    fetch('/api/evaluate', {
        method: 'POST',
        body: formData // No headers needed, fetch sets multipart/form-data automatically
    })
    .then(response => response.json())
    .then(data => {
        // Reset button
        btn.innerHTML = 'Evaluate Content';
        btn.disabled = false;

        // Show results
        resultsSection.style.display = 'block';
        
        if (data.status === 'success') {
            resultsSection.innerHTML = `
                <div class="alert alert-success">
                    <h4>✅ Success!</h4>
                    <p><strong>Source:</strong> ${data.source}</p>
                    <p><strong>Character Count:</strong> ${data.extracted_characters}</p>
                </div>
                <h5>Extracted Text Preview:</h5>
                <div class="p-3 bg-white border rounded" style="max-height: 200px; overflow-y: auto;">
                    ${data.preview}
                </div>
            `;
        } else {
            resultsSection.innerHTML = `
                <div class="alert alert-danger">
                    <strong>Error:</strong> ${data.message}
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while processing the request.");
        btn.innerHTML = 'Evaluate Content';
        btn.disabled = false;
    });
});