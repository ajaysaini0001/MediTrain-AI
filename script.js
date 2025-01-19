document.addEventListener('DOMContentLoaded', function() {
    const symptomsInput = document.getElementById('symptoms-input');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const questionsSection = document.querySelector('.questions-section');
    const questionsContainer = document.getElementById('questions-container');
    const submitAnswersBtn = document.getElementById('submit-answers-btn');
    const resultsSection = document.querySelector('.results-section');
    const loadingOverlay = document.querySelector('.loading-overlay');
    const diseaseResult = document.querySelector('#disease-result p');
    const treatmentResult = document.querySelector('#treatment-result p');

    let currentSymptoms = '';
    let additionalInfo = {};

    // Voice Input Handler
    voiceInputBtn.addEventListener('click', async function() {
        try {
            loadingOverlay.style.display = 'flex';
            const response = await fetch('/voice-input', {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                symptomsInput.value = data.text;
            } else {
                alert('Error processing voice input. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing voice input. Please try again.');
        } finally {
            loadingOverlay.style.display = 'none';
        }
    });

    // Create a question element
    function createQuestionElement(question) {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-item';
        
        const questionText = document.createElement('p');
        questionText.textContent = `${question.symptom}: ${question.question}`;
        questionDiv.appendChild(questionText);

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'question-input';
        input.dataset.symptom = question.symptom;
        input.dataset.relatedSymptom = question.related_symptom;
        questionDiv.appendChild(input);

        return questionDiv;
    }

    // Analyze Symptoms Handler
    analyzeBtn.addEventListener('click', async function() {
        currentSymptoms = symptomsInput.value.trim().toLowerCase();
        
        if (!currentSymptoms) {
            alert('Please enter your symptoms first.');
            return;
        }

        try {
            loadingOverlay.style.display = 'flex';
            const response = await fetch('/get-questions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symptoms: currentSymptoms })
            });
            
            const data = await response.json();
            
            if (data.success && data.questions && data.questions.length > 0) {
                // Clear previous questions
                questionsContainer.innerHTML = '';
                
                // Add new questions
                data.questions.forEach(question => {
                    questionsContainer.appendChild(createQuestionElement(question));
                });
                
                // Show questions section
                questionsSection.style.display = 'block';
                resultsSection.style.display = 'none';
                
                // Smooth scroll to questions
                questionsSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                // If no follow-up questions, proceed directly to prediction
                submitPrediction();
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error analyzing symptoms. Please try again.');
        } finally {
            loadingOverlay.style.display = 'none';
        }
    });

    // Submit Answers Handler
    submitAnswersBtn.addEventListener('click', async function() {
        // Collect answers
        const inputs = questionsContainer.querySelectorAll('.question-input');
        additionalInfo = {};
        
        inputs.forEach(input => {
            if (input.value.trim()) {
                additionalInfo[input.dataset.relatedSymptom] = input.value.trim();
            }
        });

        await submitPrediction();
    });

    // Submit final prediction
    async function submitPrediction() {
        try {
            loadingOverlay.style.display = 'flex';
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symptoms: currentSymptoms,
                    additional_info: additionalInfo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                diseaseResult.textContent = data.disease;
                treatmentResult.textContent = data.treatment;
                resultsSection.style.display = 'grid';
                questionsSection.style.display = 'none';
                
                // Save to history
                saveToHistory({
                    symptoms: currentSymptoms,
                    disease: data.disease,
                    treatment: data.treatment,
                    timestamp: new Date().toISOString()
                });
                
                // Smooth scroll to results
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Error analyzing symptoms. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error analyzing symptoms. Please try again.');
        } finally {
            loadingOverlay.style.display = 'none';
        }
    }

    // Save prediction to history
    function saveToHistory(data) {
        try {
            fetch('/save-history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
        } catch (error) {
            console.error('Error saving to history:', error);
        }
    }

    // Add input validation
    symptomsInput.addEventListener('input', function() {
        const maxLength = 500;
        if (this.value.length > maxLength) {
            this.value = this.value.substring(0, maxLength);
        }
    });
});
