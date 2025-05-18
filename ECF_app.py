import streamlit as st
import pandas as pd
from PIL import Image
import joblib 

model = joblib.load("energy_forecast_model.pkl")

with st.sidebar:
    logo = Image.open("nalco_logo.png")
    st.image(logo,use_container_width=True)
    st.title("About")
    st.markdown("""This tool was developed as part of an industrial training project at **NALCO**.  
    It leverages machine learning to forecast energy consumption in mining operations based on:
    
    -Machine usage hours       
    -Material processed         
    -Environmental conditons        
    -Shift timings and Machine types
      """)

    st.write("**Tech Stack** : Python ,Streamlit ,Scikit-learn")
    st.write("**Model used** : Random Forest Regressor")
    st.write("**Data** :  Synthetic Industrial dataset")





st.title("Energy Consumption Forecasting")
st.subheader("Welcome to the Energy Forecasting Tool!")
st.markdown("""
This application helps you predict energy consumption based on key operational and environmental factors in mining operations. You can adjust inputs to simulate different scenarios and estimate power usage in real time.

ℹ️ To learn more check out the **About** section in the sidebar.
""")

st.header("**INSTRUCTIONS**")
st.error("step 1 : Enter the Input parameters ")
st.error("step 2 : Click **Predict** ")
st.error("step 3 : you get the Energy consumption Prediction")

st.divider()


def predict_energy(machine_hours, material_processed, temperature, humidity, shift, machine_type):

    input_data ={
        'Machine_Hours': [machine_hours],
        'Material_Processed_tons': [material_processed],
        'Temperature_C': [temperature],
        'Humidity_%': [humidity],
        #machine_type encoded

        'Machine_Type_Crusher': [1 if machine_type == 'Crusher' else 0],
        'Machine_Type_Excavator': [1 if machine_type == 'Excavator' else 0],
        'Machine_Type_Hauler': [1 if machine_type == 'Hauler' else 0],
        #shift encoded
        'Shift_Evening': [1 if shift == 'Evening' else 0],
        'Shift_Morning': [1 if shift == 'Morning' else 0],
        'Shift_Night': [1 if shift == 'Night' else 0],

    }

    input_df = pd.DataFrame(input_data)
    with st.expander("Input DataFrame"):
        st.write(input_df)


    if machine_hours == 0:
        return 0
    else:
        prediction = model.predict(input_df)[0]
        return prediction
# here we are using [0] as predict method gives a numpy array as output 
# but we only have one value therefore we take the 1st element only
    



machine_hours = st.number_input("**How many hours does the machine run** ")

material_processed = st.number_input("**How much material is processed** (in tons)")

temperature = st.slider("**What is the temperature** (in Celsius) ", -10.0 ,50.0,25.0)

humidity = st.slider("**What is Humidity** % ", 0.0 , 100.0, 50.0)

shift = st.selectbox("**Select the shift**",["Morning","Evening","Night"])

machine_type = st.selectbox("**Select the machine** ",["Hauler","Crusher","Excavator"])

if(st.button("**Predict**")):
    st.divider()
    res = predict_energy(machine_hours ,material_processed,temperature,humidity,shift,machine_type)
    st.success(f"Predicted Energy Consumption: {res:.2f} kWh")


