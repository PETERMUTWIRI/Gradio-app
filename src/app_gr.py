
import gradio as gr
from gradio.components import Number, Dropdown
import numpy as np
import pandas as pd
import pickle

# Load exported data
exported_data_path = 'src\Asset\ML\my_exported_components.pkl'
with open(exported_data_path, 'rb') as file:
    exported_data = pickle.load(file)

# Load the exported components
categorical_imputer = exported_data['categorical_imputer']
numerical_imputer = exported_data['numerical_imputer']
encoder = exported_data['encoder']
scaler = exported_data['scaler']
best_model = exported_data['best_model']

def churn_prediction(gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, 
                     InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
                     StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
                     MonthlyCharges, TotalCharges, MonthlyCharges_TotalCharges_Ratio, AverageMonthlyCharges):
    
    # Create a DataFrame with the provided inputs
    prediction_data = pd.DataFrame({
        'gender': [gender],
        'SeniorCitizen': [SeniorCitizen],
        'Partner': [Partner],
        'Dependents': [Dependents],
        'tenure': [tenure],
        'PhoneService': [PhoneService],
        'MultipleLines': [MultipleLines],
        'InternetService': [InternetService],
        'OnlineSecurity': [OnlineSecurity],
        'OnlineBackup': [OnlineBackup],
        'DeviceProtection': [DeviceProtection],
        'TechSupport': [TechSupport],
        'StreamingTV': [StreamingTV],
        'StreamingMovies': [StreamingMovies],
        'Contract': [Contract],
        'PaperlessBilling': [PaperlessBilling],
        'PaymentMethod': [PaymentMethod],
        'MonthlyCharges': [MonthlyCharges],
        'TotalCharges': [TotalCharges],
        'MonthlyCharges_TotalCharges_Ratio': [MonthlyCharges_TotalCharges_Ratio],
        'AverageMonthlyCharges': [AverageMonthlyCharges]
    })
    
    # Preprocessing for categorical data
    prediction_data_categorical = prediction_data.select_dtypes(include='object')
    prediction_data_encoded = encoder.transform(categorical_imputer.transform(prediction_data_categorical))

    # Convert the encoded sparse matrix to a DataFrame
    prediction_data_encoded_df = pd.DataFrame.sparse.from_spmatrix(prediction_data_encoded,
                                                                  columns=encoder.get_feature_names_out(prediction_data_categorical.columns),
                                                                  index=prediction_data_categorical.index)

    # Preprocessing for numerical data
    prediction_data_numerical = prediction_data.select_dtypes(include=['int', 'float'])
    prediction_data_scaled = scaler.transform(numerical_imputer.transform(prediction_data_numerical))

    # Convert the scaled numerical data to a DataFrame
    prediction_data_scaled_df = pd.DataFrame(prediction_data_scaled,
                                             columns=prediction_data_numerical.columns,
                                             index=prediction_data_numerical.index)

    # Concatenate the encoded categorical data and scaled numerical data
    prediction_data_preprocessed = pd.concat([prediction_data_encoded_df, prediction_data_scaled_df], axis=1)

    # Make predictions using the loaded model
    predictions = best_model.predict(prediction_data_preprocessed)

    # Map the predictions to 'Yes' or 'No'
    prediction_label = 'Customer Churn' if predictions[0] == 1 else 'Customer Not Churn'

    
    return prediction_label


# Define input components
input_components = [
    gr.Dropdown(choices=['Female', 'Male'], label='gender: Select the gender of the customer.'),
    gr.Dropdown(choices=['No', 'Yes'], label='SeniorCitizen: Select if the customer is a senior citizen.'),
    gr.Dropdown(choices=['No', 'Yes'], label='Partner: Select if the customer has a partner.'),
    gr.Dropdown(choices=['No', 'Yes'], label='Dependents: Select if the customer has dependents.'),
    gr.Number(label='tenure: Enter the number of months the customer has been with the company.', minimum=0, maximum=72),
    gr.Dropdown(choices=['No', 'Yes'], label='PhoneService: Select if the customer has a phone service.'),
    gr.Dropdown(choices=['No', 'Yes'], label='MultipleLines: Select if the customer has multiple lines.'),
    gr.Dropdown(choices=['DSL', 'Fiber optic', 'No'], label='InternetService: Select the type of internet service.'),
    gr.Dropdown(choices=['No', 'Yes'], label='OnlineSecurity: Select if the customer has online security.'),
    gr.Dropdown(choices=['No', 'Yes'], label='OnlineBackup: Select if the customer has online backup.'),
    gr.Dropdown(choices=['No', 'Yes'], label='DeviceProtection: Select if the customer has device protection.'),
    gr.Dropdown(choices=['No', 'Yes'], label='TechSupport: Select if the customer has tech support.'),
    gr.Dropdown(choices=['No', 'Yes'], label='StreamingTV: Select if the customer has streaming TV.'),
    gr.Dropdown(choices=['No', 'Yes'], label='StreamingMovies: Select if the customer has streaming movies.'),
    gr.Dropdown(choices=['Month-to-month', 'One year', 'Two year'], label='Contract: Select the contract type.'),
    gr.Dropdown(choices=['No', 'Yes'], label='PaperlessBilling: Select if the customer uses paperless billing.'),
    gr.Dropdown(choices=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], label='PaymentMethod: Select the payment method.'),
    gr.Number(label='MonthlyCharges: Enter the monthly charges for the customer.', minimum=18, maximum=119),
    gr.Number(label='TotalCharges: Enter the total charges for the customer.', minimum=19, maximum=8670),
    gr.Slider(label='MonthlyCharges_TotalCharges_Ratio: Enter the ratio of monthly charges to total charges.', minimum=0.00, maximum=1.0),
    gr.Number(label='AverageMonthlyCharges: Enter the average monthly charges for the customer.', minimum=0, maximum=120)
]



# Create and launch the Gradio interface
iface = gr.Interface(
    fn=churn_prediction,
    inputs=input_components,
    outputs="text",
    title="Customer Churn Prediction", 
    description="This app Predict customer churn using machine learning. It Provides stakeholders & Customers information to predict whether they are likely to leave(Churn) a telecommunications company or stay.",
    live=False,  
    # share=True
)

iface.launch()
