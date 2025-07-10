import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
from imblearn.over_sampling import SMOTE

df = pd.read_csv('data/Final_heart_dataset.csv')

final_features = [
    'age', 'chol_log', 'oldpeak_log', 'trestbps_log', 'thalach_sq', 'sex_1',
    'cp_1', 'cp_2', 'cp_3', 'fbs_1', 'restecg_1', 'restecg_2', 'exang_1',
    'slope_1', 'slope_2', 'ca_1', 'ca_2', 'ca_3', 'thal_2', 'thal_3'
]

X = df[final_features]
Y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=None
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, 'model/heart_disease_model.pkl')
