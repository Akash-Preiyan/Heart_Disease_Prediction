from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import numpy as np

app = Flask(__name__)

# Load and prepare the model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

def prepare_model():
    # Load your dataset
    df = pd.read_csv(r"C:\Users\akash\OneDrive\Desktop\Projects\Heart_Disease_Prediction\Dataset\heart.csv")  # Update with your dataset path
    
    # Separate features and target
    X = df[['thalach', 'oldpeak', 'cp', 'ca', 'exang', 'chol', 'age', 'trestbps', 'slope', 'sex']]
    y = df['target']  # Assuming you have a target column for heart disease
    
    # Split and scale data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # Ensure you scale the test set as well
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Predict labels and probabilities
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]  # Use probability estimates for ROC-AUC
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    
    # Calculate ROC-AUC score
    auc = roc_auc_score(y_test, y_proba)
    print(f"ROC-AUC Score: {auc:.2f}")
    
    return model, scaler

# Call the function to train the model and print the results
model, scaler = prepare_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from the form
        features = {
            'thalach': float(request.form['thalach']),
            'oldpeak': float(request.form['oldpeak']),
            'cp': int(request.form['cp']),
            'ca': int(request.form['ca']),
            'exang': int(request.form['exang']),
            'chol': float(request.form['chol']),
            'age': int(request.form['age']),
            'trestbps': float(request.form['trestbps']),
            'slope': int(request.form['slope']),
            'sex': int(request.form['sex'])
        }
        
        # Convert to array and scale
        input_features = np.array(list(features.values())).reshape(1, -1)
        input_features_scaled = scaler.transform(input_features)
        
        # Get prediction probability
        prediction_proba = model.predict_proba(input_features_scaled)[0][1] * 100
        
        return jsonify({
            'success': True,
            'prediction': round(prediction_proba, 2)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)