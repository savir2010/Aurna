import numpy as np
from tensorflow.keras.models import load_model # type: ignore
from generate_data import collect_muse_eeg_csv
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder


# Load the pre-trained model
model = load_model('eeg_disorder_model.h5')


# Define a route for prediction
def predict_disorder():
    clean_df = pd.read_csv("cleaned_df.csv")
    collect_muse_eeg_csv(duration=10)
    inputdf = pd.read_csv("muse_eeg.csv")
    predictions = model.predict(inputdf)
    print("predicted")
    y = clean_df['disorder'].values  # Ensure it's a NumPy array
    y = y.ravel()  # Flatten it to 1D if necessary

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Ensure `predictions[0][0]` is an integer
    output = label_encoder.inverse_transform([int(predictions[0][0])])[0]

    return output


