import os
import dotenv
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

from paeio.path import path_join

dotenv.load_dotenv()

model = pd.read_pickle(
    path_join(
        os.path.dirname(os.path.abspath('../streamlit-test/models/heart_model.pkl')),
        "heart_model.pkl"
    )
)


def app(model: RandomForestClassifier):
    cols = model.feature_names_in_

    st.title("Heart Attack Predictor")
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Heart Attack Prediction App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    age = st.text_input("Age", "0")
    sex = st.selectbox("Sex", ["0", "1"])
    cp = st.selectbox("Chest Pain", ["0", "1"])
    trtbps = st.text_input("Blood pressure while resting", "0")
    chol = st.selectbox("Cholesterol", "0")
    thalachh = st.text_input("Max heart rate", "0")
    oldpeak = st.selectbox("Previous peak", "0")
    slp = st.selectbox("Slope", ["0", "1", "2"])
    caa = st.selectbox("Number of major vessels", ["0", "1", "2", "3", "4"])
    thall = st.selectbox("Thal rate", ["0", "1", "2", "3"])

    if st.button("Predict"):
        data = {
            'age': float(age),
            'sex': float(sex),
            'cp': float(cp),
            'trtbps': int(trtbps),
            'chol': int(chol),
            'thalachh': int(thalachh),
            'oldpeak': int(oldpeak),
            'slp': int(slp),
            'caa': int(caa),
            'thall': int(thall),
        }
        print(data)
        df = pd.DataFrame([list(data.values())], columns=cols)

        features_list = df.values.tolist()
        prediction = model.predict_proba(features_list)[:,1].round(4)*100



        st.success(f"Probability of heart attack: {prediction[0]}%")


if __name__=='__main__':
    app(model)
