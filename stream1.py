import streamlit as st
import pandas as pd
import pickle

#reading the dfs
fe_df=pd.read_excel('feature.xlsx')
encode_df=pd.read_excel('encoded.xlsx')

#for navigation box
st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', ['Home', 'Main Page'])

#first page
if selection == 'Home':
    st.title('**CarDekho**')
    st.write("**Best Place to buy New and Used Cars in India**")
    st.image(r"C:\Users\Dharshinee R\Desktop\CarDekho-Feature.jpg", use_container_width=True)

#Second page
if selection == 'Main Page':
    st.title('**Know Used Car Price**')
    col1, col2, col3 = st.columns([5,5,5])#dividing among columns
    
    with col1:
     City = st.selectbox('Choose a City', fe_df['City'].unique())
     Vehicle_Age = st.number_input("Select Vehicle Age", 1, 17, step=1)
     transmission_Manual = st.selectbox("Select the Transmission Type:", fe_df['transmission_Manual'].unique())
    with col2:
     Car_Brand = st.selectbox("Select a Car Brand", fe_df['Car_Brand'].unique())
     Engine_Displacement= st.slider("Select Engine CC", 700, 2000, step=50)
     Car_color=st.selectbox("Select the Color of the car",fe_df['Car_Color'].unique())
    with col3:    
     km=st.slider("Select the Kms Driven",0,975000,step=1000)
     Ownership=st.selectbox("Select the Ownership",fe_df['Ownership'].unique())
   
   
   #creating a input dataframe 
    input_data = pd.DataFrame({
        'Car_Brand': [Car_Brand],
        'Vehicle_Age': [Vehicle_Age],
        'transmission_Manual': [transmission_Manual],
        'Engine Displacement': [Engine_Displacement],
        'City': [City],
        'km':[km],
        'Car_Color':[Car_color],
        'Ownership':[Ownership]
})

    #mapping the encoded df with feature df 
    input_data['Car_Brand'] = input_data['Car_Brand'].apply(lambda x: encode_df['Car_Brand'][fe_df['Car_Brand'] == x].values[0])
    input_data['transmission_Manual'] = input_data['transmission_Manual'].apply(lambda x: encode_df['transmission_Manual'][fe_df['transmission_Manual'] == x].values[0])
    input_data['City'] = input_data['City'].apply(lambda x: encode_df['City'][fe_df['City'] == x].values[0])
    input_data['Car_Color'] = input_data['Car_Color'].apply(lambda x: encode_df['Car_Color'][fe_df['Car_Color'] == x].values[0])
    input_data['Ownership']=input_data['Ownership'].apply(lambda x :encode_df['Ownership'][fe_df['Ownership']==x].values[0])
   
    #loading the pickle file with the model
    with open('gbr2.pkl', 'rb') as file: 
      model = pickle.load(file) 
      
# Make a prediction 
    if st.button('Predict Price'):
     prediction = model.predict(input_data) 
     st.write(f'The estimated price of the car is: ₹ {prediction[0]:,.2f}')


