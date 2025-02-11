import pandas as pd
import numpy as np
from flask_cors import CORS 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify
import joblib
import os

# Create Flask app
app = Flask(__name__)
CORS(app)

def load_data():
    """Load and preprocess the lawyer and case data"""
    # Check if CSV files exist
    if not os.path.exists('D:\Legal case ml\dataset\lawyers_data.csv') or not os.path.exists('D:\Legal case ml\dataset\past_cases_data.csv'):
        raise FileNotFoundError("CSV files not found. Please run the data generation script first.")
    
    # Load the data
    lawyers_df = pd.read_csv('D:\Legal case ml\dataset\lawyers_data.csv')
    past_cases_df = pd.read_csv('D:\Legal case ml\dataset\past_cases_data.csv')
    
    return lawyers_df, past_cases_df

# Load the data
try:
    lawyers_df, past_cases_df = load_data()
    print(f"Loaded {len(lawyers_df)} lawyers and {len(past_cases_df)} past cases")
except Exception as e:
    print(f"Error loading data: {str(e)}")
    raise

# Initialize TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
# Fit the TF-IDF vectorizer with the lawyer descriptions
tfidf.fit(lawyers_df['description'])

def prepare_features(past_cases_df, lawyers_df):
    """Prepare features for the prediction model using real data"""
    # Merge past cases with lawyer information
    features_df = past_cases_df.merge(
        lawyers_df[['lawyer_id', 'experience_years', 'feedback_score', 'cases_handled']],
        on='lawyer_id'
    )
    
    # Create feature matrix
    X = pd.DataFrame({
        'experience_years': features_df['experience_years'],
        'feedback_score': features_df['feedback_score'],
        'cases_handled': features_df['cases_handled'],
        'case_duration_months': features_df['case_duration_months'],
        'complexity_score': features_df['complexity_score'],
        'case_type': features_df['case_type']
    })
    
    # Create target variable (1 for 'won', 0 for 'lost')
    y = (features_df['outcome'] == 'won').astype(int)
    
    return X, y

def train_prediction_model(X, y):
    """Train the success prediction model using real data"""
    # Convert categorical variables to numerical
    X = pd.get_dummies(X, columns=['case_type'])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Print model accuracy
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    print(f"Model Training Accuracy: {train_accuracy:.3f}")
    print(f"Model Testing Accuracy: {test_accuracy:.3f}")
    
    return model

# Prepare features and train model
X, y = prepare_features(past_cases_df, lawyers_df)
prediction_model = train_prediction_model(X, y)

@app.route('/recommend_lawyers', methods=['POST'])
def recommend_lawyers():
    """API endpoint to recommend lawyers based on case type and description"""
    try:
        print("Received request for lawyer recommendation.")

        data = request.get_json()
        print("Received JSON data:", data)  # Debug print

        if not data:
            print("Error: No JSON data provided.")
            return jsonify({'error': 'No JSON data provided'}), 400

        case_type = data.get('case_type')
        case_description = data.get('description')
        print(f"Case Type: {case_type}, Case Description: {case_description}")  # Debug print

        if not case_type or not case_description:
            print("Error: Missing required fields: case_type and description.")
            return jsonify({'error': 'Missing required fields: case_type and description'}), 400

        # Vector for the new case
        case_vector = tfidf.transform([case_description])
        print("Generated case vector.")  # Debug print

        # Calculate similarity scores
        similarity_scores = cosine_similarity(case_vector, tfidf.transform(lawyers_df['description']))[0]
        print("Calculated similarity scores.")  # Debug print

        # Filter lawyers by specialization matching case type
        matching_lawyers = lawyers_df[lawyers_df['specialization'].str.contains(case_type, case=False)].copy()
        print(f"Found {len(matching_lawyers)} matching lawyers.")  # Debug print

        if matching_lawyers.empty:
            print(f"No lawyers found matching case type: {case_type}")
            return jsonify({'error': f'No lawyers found matching case type: {case_type}'}), 404

        # Add similarity scores to matching lawyers
        matching_lawyers['similarity_score'] = similarity_scores[matching_lawyers.index]
        print("Added similarity scores to matching lawyers.")  # Debug print

        # Calculate success rate from past cases
        lawyer_success_rates = past_cases_df.groupby('lawyer_id').agg({
            'outcome': lambda x: (x == 'won').mean()
        }).rename(columns={'outcome': 'actual_success_rate'})

        print("Calculated success rates from past cases.")  # Debug print

        # Merge success rates
        matching_lawyers = matching_lawyers.merge(
            lawyer_success_rates,
            left_on='lawyer_id',
            right_index=True,
            how='left'
        )

        print("Merged success rates with lawyer data.")  # Debug print

        # Calculate overall score
        matching_lawyers['overall_score'] = (
            matching_lawyers['similarity_score'] * 0.3 +
            matching_lawyers['actual_success_rate'] * 0.4 +
            matching_lawyers['feedback_score'] / 5 * 0.3
        )

        print("Calculated overall scores.")  # Debug print

        # Sort by overall score and get top recommendations
        top_recommendations = matching_lawyers.nlargest(3, 'overall_score')
        print(f"Top {len(top_recommendations)} recommendations selected.")  # Debug print

        # Prepare response with description
        recommendations = []
        for _, lawyer in top_recommendations.iterrows():
            # Get recent cases for this lawyer
            recent_cases = past_cases_df[ 
                (past_cases_df['lawyer_id'] == lawyer['lawyer_id']) & 
                (past_cases_df['case_type'] == case_type)
            ].tail(3)

            recommendations.append({
                'lawyer_id': int(lawyer['lawyer_id']),
                'name': lawyer['name'],
                'specialization': lawyer['specialization'],
                'description': lawyer['description'],  # Add description here
                'experience_years': int(lawyer['experience_years']),
                'success_rate': float(lawyer['actual_success_rate']),
                'feedback_score': float(lawyer['feedback_score']),
                'similarity_score': float(lawyer['similarity_score']),
                'overall_score': float(lawyer['overall_score']),
                'hourly_rate': int(lawyer['hourly_rate']),
                'location': lawyer['location'],
                'law_school': lawyer['law_school'],
                'recent_cases': len(recent_cases),
                'pro_bono_cases': int(lawyer['pro_bono_cases'])
            })

        print("Returning recommendations:", recommendations)  # Debug print

        return jsonify({
            'recommendations': recommendations
        })

    except Exception as e:
        print("Error:", str(e))  # Debug print for errors
        return jsonify({'error': f'Server error: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
