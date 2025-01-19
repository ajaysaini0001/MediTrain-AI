from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import speech_recognition as sr
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load the datasets
try:
    symptoms_df = pd.read_csv('data/symptoms.csv')
    treatments_df = pd.read_csv('data/treatments.csv')
    questions_df = pd.read_csv('data/follow_up_questions.csv')
    logger.info(f"Loaded datasets - Symptoms: {len(symptoms_df)} rows, Treatments: {len(treatments_df)} rows, Questions: {len(questions_df)} rows")
except Exception as e:
    logger.error(f"Error loading datasets: {str(e)}")
    raise

# Initialize models
class MediTrainAI:
    def __init__(self):
        self.disease_pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', MultinomialNB())
        ])
        self.treatment_pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', MultinomialNB())
        ])
        self.symptom_questions = {}
        self.train_models()
        self.symptom_questions = self._prepare_questions()
    
    def _prepare_questions(self):
        questions_dict = {}
        try:
            for _, row in questions_df.iterrows():
                symptom = row['Symptom'].lower().strip()
                if symptom not in questions_dict:
                    questions_dict[symptom] = []
                questions_dict[symptom].append({
                    'question': row['Question'],
                    'related_symptom': row['Related_Symptoms']
                })
            logger.info(f"Prepared questions for {len(questions_dict)} symptoms")
            return questions_dict
        except Exception as e:
            logger.error(f"Error preparing questions: {str(e)}")
            return {}
    
    def get_follow_up_questions(self, symptoms):
        try:
            relevant_questions = []
            symptoms_list = [s.strip().lower() for s in symptoms.split(',')]
            logger.debug(f"Processing symptoms: {symptoms_list}")
            
            for symptom in symptoms_list:
                if symptom in self.symptom_questions:
                    for q in self.symptom_questions[symptom]:
                        relevant_questions.append({
                            'symptom': symptom,
                            'question': q['question'],
                            'related_symptom': q['related_symptom']
                        })
            
            logger.info(f"Found {len(relevant_questions)} relevant questions for symptoms")
            return relevant_questions
        except Exception as e:
            logger.error(f"Error getting follow-up questions: {str(e)}")
            return []
    
    def train_models(self):
        try:
            # Train disease prediction model
            self.disease_pipeline.fit(symptoms_df['Symptoms'], symptoms_df['Disease'])
            logger.info("Trained disease prediction model")
            
            # Train treatment prediction model
            self.treatment_pipeline.fit(treatments_df['Disease'], treatments_df['Treatment'])
            logger.info("Trained treatment prediction model")
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            raise
    
    def predict_disease(self, symptoms, additional_info=None):
        try:
            if additional_info:
                # Enhance symptoms with additional information
                enhanced_symptoms = f"{symptoms} with {', '.join(f'{k}: {v}' for k, v in additional_info.items())}"
            else:
                enhanced_symptoms = symptoms
                
            predicted_disease = self.disease_pipeline.predict([enhanced_symptoms])[0]
            logger.info(f"Predicted disease: {predicted_disease}")
            return predicted_disease
        except Exception as e:
            logger.error(f"Error predicting disease: {str(e)}")
            raise
    
    def predict_treatment(self, disease):
        try:
            predicted_treatment = self.treatment_pipeline.predict([disease])[0]
            logger.info(f"Predicted treatment: {predicted_treatment}")
            return predicted_treatment
        except Exception as e:
            logger.error(f"Error predicting treatment: {str(e)}")
            raise

# Initialize the AI model
try:
    meditrain_ai = MediTrainAI()
except Exception as e:
    logger.error(f"Error initializing MediTrainAI: {str(e)}")
    raise

# Initialize history storage
consultation_history = []

# Speech recognition function
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return "Could not understand audio"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html', history=consultation_history)

@app.route('/save-history', methods=['POST'])
def save_history():
    try:
        data = request.get_json()
        consultation_history.append(data)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error saving to history: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-questions', methods=['POST'])
def get_questions():
    try:
        data = request.get_json()
        symptoms = data['symptoms']
        logger.debug(f"Received request for questions with symptoms: {symptoms}")
        
        # Get relevant follow-up questions
        questions = meditrain_ai.get_follow_up_questions(symptoms)
        logger.info(f"Returning {len(questions)} questions")
        
        return jsonify({
            'success': True,
            'questions': questions
        })
    except Exception as e:
        logger.error(f"Error in get_questions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        symptoms = data['symptoms']
        additional_info = data.get('additional_info', None)
        logger.debug(f"Received prediction request - Symptoms: {symptoms}, Additional Info: {additional_info}")
        
        # Predict disease with enhanced information
        predicted_disease = meditrain_ai.predict_disease(symptoms, additional_info)
        
        # Predict treatment
        predicted_treatment = meditrain_ai.predict_treatment(predicted_disease)
        
        return jsonify({
            'success': True,
            'disease': predicted_disease,
            'treatment': predicted_treatment
        })
    except Exception as e:
        logger.error(f"Error in predict: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/voice-input', methods=['POST'])
def voice_input():
    try:
        text = speech_to_text()
        return jsonify({
            'success': True,
            'text': text
        })
    except Exception as e:
        logger.error(f"Error in voice_input: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
