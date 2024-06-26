import dotenv
import pandas as pd
import streamlit as st

from paeio import io
from xgboost import XGBClassifier

dotenv.load_dotenv()

try:
    model = io.read_any(
        'https://testmlopaes.dfs.core.windows.net/testing/refined/deploy/fraud_model.pkl',
        func=pd.read_pickle
    )
except:
    model = pd.read_pickle("src/output/fraud_model.pkl")


def app(model: XGBClassifier):
    cols = model.feature_names_in_

    st.title("Fraud Predictor")
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Fraud Prediction App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)

    distance_from_home = st.text_input("distance_from_home","0")
    distance_from_last_transaction = st.text_input("distance_from_last_transaction", "0")
    ratio_to_median_purchase_price = st.text_input("ratio_to_median_purchase_price", "0")
    repeat_retailer = st.selectbox("repeat_retailer",["0", "1"])
    used_chip = st.selectbox("used_chip",["0", "1"])
    used_pin_number = st.selectbox("used_pin_number",["0", "1"])
    online_order = st.selectbox("online_order",["0", "1"])

    if st.button("Predict"):
        data = {
            'distance_from_home': float(distance_from_home),
            'distance_from_last_transaction': float(distance_from_last_transaction),
            'ratio_to_median_purchase_price': float(ratio_to_median_purchase_price),
            'repeat_retailer': int(repeat_retailer),
            'used_chip': int(used_chip),
            'used_pin_number': int(used_pin_number),
            'online_order': int(online_order),
        }
        print(data)
        df = pd.DataFrame([list(data.values())], columns=cols)

        features_list = df.values.tolist()
        prediction = model.predict(features_list)

        output = int(prediction[0])
        if output == 1:
            text = "Fraudent Transaction"
        else:
            text = "Non-Fraudent Transaction"

        st.success(text)


if __name__=='__main__':
    app(model)
