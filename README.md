# MediTrain AI

## 🏥 Overview
MediTrain AI is an intelligent medical consultation system that uses machine learning to analyze symptoms, provide interactive follow-up questions, and suggest possible diagnoses with treatments. The system is designed to assist users in understanding their medical conditions while emphasizing the importance of professional medical consultation.

## 🌟 Features

### 1. Symptom Analysis
- Text-based symptom input
- Voice input support
- Natural language processing for symptom understanding

### 2. Interactive Questioning
- Dynamic follow-up questions based on initial symptoms
- Specialized questions for different medical conditions
- Comprehensive coverage of various symptoms

### 3. AI-Powered Predictions
- Machine learning-based disease prediction
- Treatment recommendations
- Severity assessment

### 4. User-Friendly Interface
- Clean, modern design
- Responsive layout
- Easy navigation
- Consultation history tracking

## 🛠️ Technology Stack

### Backend
- Python 3.x
- Flask (Web Framework)
- scikit-learn (Machine Learning)
- pandas (Data Processing)
- NumPy (Numerical Operations)
- SpeechRecognition (Voice Input)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Font Awesome (Icons)
- Google Fonts

### Data
- Symptoms dataset
- Treatments dataset
- Follow-up questions dataset
- Symptom severity data
- Symptom descriptions
- Preventive measures

## 📋 Prerequisites
```bash
- Python 3.x
- pip (Python package manager)
- Modern web browser
- Internet connection (for CDN resources)
```

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/ajaysaini0001/MediTrain-AI.git
cd MediTrain-AI
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Access the application
```
Open your browser and navigate to: http://localhost:5000
```

## 📁 Project Structure
```
MediTrain-AI/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── data/                    # Dataset directory
│   ├── symptoms.csv         # Symptom-disease mappings
│   ├── treatments.csv       # Disease-treatment mappings
│   ├── follow_up_questions.csv  # Dynamic questioning system
│   ├── Symptom-severity.csv    # Symptom severity ratings
│   ├── symptom_Description.csv # Detailed symptom descriptions
│   └── symptom_precaution.csv # Preventive measures
├── static/
│   ├── css/
│   │   └── style.css       # Application styling
│   └── js/
│       └── script.js       # Frontend logic
└── templates/
    ├── index.html          # Main application interface
    └── history.html        # Consultation history page
```

## 💻 Usage

1. **Enter Symptoms**
   - Type symptoms in the text box
   - Or use voice input by clicking the microphone button

2. **Answer Questions**
   - Respond to follow-up questions for better accuracy
   - Provide additional details when prompted

3. **View Results**
   - See predicted condition
   - View recommended treatment
   - Read important medical disclaimers

4. **Check History**
   - Access past consultations
   - Review previous symptoms and diagnoses

## ⚠️ Important Disclaimers

1. **Not a Replacement for Professional Medical Advice**
   - This system is for educational and informational purposes only
   - Always consult healthcare professionals for medical advice
   - Do not use for emergency medical situations

2. **Accuracy Limitations**
   - Predictions are based on training data
   - Results may not cover all possible conditions
   - System continues to learn and improve

3. **Privacy Notice**
   - No personal health information is stored permanently
   - Session data is cleared on server restart
   - Use discretion when entering sensitive information

## 🔄 Future Enhancements

1. **Technical Improvements**
   - Enhanced ML models
   - Additional symptom datasets
   - Real-time learning capabilities

2. **Feature Additions**
   - User authentication
   - Persistent data storage
   - Export functionality
   - Multilingual support

3. **Integration Possibilities**
   - Medical knowledge bases
   - Healthcare provider networks
   - Emergency service contacts

## 👥 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. Visit our [GitHub repository](https://github.com/ajaysaini0001/MediTrain-AI) for more information.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Medical datasets from reputable sources
- Open-source ML libraries
- Flask framework community
- Frontend design inspirations

## 📞 Support
For support:
- Create an issue in the [GitHub repository](https://github.com/ajaysaini0001/MediTrain-AI/issues)
- Contact: ajaysaini9399@gmail.com

---
⚕️ Built with care by Ajay Saini for educational purposes.
