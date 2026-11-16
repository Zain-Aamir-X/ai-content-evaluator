document.addEventListener('DOMContentLoaded', () => {
    
    const submitBtn = document.getElementById('submitBtn');
    const resultsSection = document.getElementById('resultsSection');

    submitBtn.addEventListener('click', function() {
        const textInput = document.getElementById('textInput').value.trim();
        const fileInput = document.getElementById('fileInput').files[0];
        
        // 1. Validate input (ensure user provided text or a file)
        if (!textInput && !fileInput) {
            alert("Please paste some text or upload a file first.");
            return;
        }

        // 2. Prepare the data payload
        const formData = new FormData();
        if (fileInput) {
            // Check file size (5MB = 5 * 1024 * 1024 bytes)
            if (fileInput.size > 5 * 1024 * 1024) {
                alert("Error: File is too large. Maximum size is 5MB.");
                return;
            }
            formData.append('file', fileInput);
        } else {
            formData.append('text', textInput);
        }

        // 3. Set Loading State
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        submitBtn.disabled = true;
        
        // Hide old results and show a loading message
        resultsSection.style.display = 'block';
        resultsSection.innerHTML = `
            <div class="text-center my-4">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;"></div>
                <p class="mt-3 text-muted">Analyzing content for developmental suitability...</p>
            </div>
        `;

        // 4. Send to backend API
        fetch('/api/evaluate', {
            method: 'POST',
            body: formData // Fetch automatically sets multipart/form-data headers
        })
        .then(response => response.json())
        .then(data => {
            // Reset button state
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;

            // 5. Handle the Response
            if (data.status === 'success') {
                const res = data.results;
                
                // Helper function to determine badge color based on the label
                const getBadgeClass = (label) => {
                    if (label === 'Appropriate') return 'bg-success';
                    if (label === 'Borderline') return 'bg-warning text-dark';
                    return 'bg-danger'; // Inappropriate
                };

                // Build the 4-domain Results Dashboard
                resultsSection.innerHTML = `
                    <div class="alert alert-success mt-4 shadow-sm">
                        <h4 class="alert-heading">✅ Evaluation Complete!</h4>
                        <p class="mb-0">Report ID: #${data.report_id} | Saved to database successfully.</p>
                    </div>
                    
                    <div class="row mt-3">
                        <!-- Linguistic Domain -->
                        <div class="col-md-6 mb-3">
                            <div class="card h-100 border-start border-5 border-primary shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title text-primary">Linguistic Appropriateness</h5>
                                    <span class="badge ${getBadgeClass(res.linguistic.label)} mb-2 px-3 py-2 fs-6">${res.linguistic.label}</span>
                                    <p class="card-text text-muted small mt-2">${res.linguistic.feedback}</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Cognitive Domain -->
                        <div class="col-md-6 mb-3">
                            <div class="card h-100 border-start border-5 border-info shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title text-info">Cognitive Appropriateness</h5>
                                    <span class="badge ${getBadgeClass(res.cognitive.label)} mb-2 px-3 py-2 fs-6">${res.cognitive.label}</span>
                                    <p class="card-text text-muted small mt-2">${res.cognitive.feedback}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Socio-Emotional Domain -->
                        <div class="col-md-6 mb-3">
                            <div class="card h-100 border-start border-5 border-success shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title text-success">Socio-Emotional Suitability</h5>
                                    <span class="badge ${getBadgeClass(res.socio_emotional.label)} mb-2 px-3 py-2 fs-6">${res.socio_emotional.label}</span>
                                    <p class="card-text text-muted small mt-2">${res.socio_emotional.feedback}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Moral Domain -->
                        <div class="col-md-6 mb-3">
                            <div class="card h-100 border-start border-5 border-secondary shadow-sm">
                                <div class="card-body">
                                    <h5 class="card-title text-secondary">Moral Safety</h5>
                                    <span class="badge ${getBadgeClass(res.moral.label)} mb-2 px-3 py-2 fs-6">${res.moral.label}</span>
                                    <p class="card-text text-muted small mt-2">${res.moral.feedback}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                // Handle API Errors (e.g., wrong file type, extraction failure)
                resultsSection.innerHTML = `
                    <div class="alert alert-danger mt-4 shadow-sm">
                        <h4 class="alert-heading">❌ Evaluation Failed</h4>
                        <p class="mb-0">${data.message}</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            // Handle Network/Server Errors
            console.error('Error:', error);
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
            
            resultsSection.innerHTML = `
                <div class="alert alert-danger mt-4 shadow-sm">
                    <h4 class="alert-heading">❌ Network Error</h4>
                    <p class="mb-0">Could not connect to the server. Please try again later.</p>
                </div>
            `;
        });
    });
});

document.getElementById('clearBtn').addEventListener('click', function() {
    document.getElementById('textInput').value = '';
    document.getElementById('fileInput').value = '';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('resultsSection').innerHTML = '';
});