
import streamlit as st
import numpy as np
import pandas as pd
import pickle


with open('final_model_xgb.pkl', 'rb') as file:
    model = pickle.load(file)


with open('transformer.pkl', 'rb') as file:
    pt = pickle.load(file)


def prediction(input_list):

    input_list = np.array(input_list, dtype = object)
    pred = model.predict_proba([input_list])[:,1][0]
    
    if pred > 0.5:
        return f'This Booking is more likely to get canceled : Chances are {round(pred,4)}'
    else:
        return f'This Booking is less likely to grt canceled : Chances are {round(pred,4)}'

def main():
    st.title('''INN HOTEL GROUP
    POWERED BY AVIRAL MEHARISHI CREATIONS ''')
    
    lt = st.text_input('PLEASE ENTER THE LEAD TIME')
    mst = (lambda x:1 if x == 'Online' else 0)(st.selectbox('ENTER THE TYPEOF BOOOKING', ['ONLINE', 'OFFLINE']))
    spcl = st.selectbox('KINDLY ENTER THE NO. OF SPECIAL REQUESTS MADE ',[0,1,2,3,4,5])
    price = st.text_input('KINDLY ENTER THE PRICE OFFERED FOR THE ROOM')
    adult = st.selectbox('SELECT THE NUMBER OF ADULTS IN THE BOOKING', [0,1,2,3,4])
    wkd = st.text_input('PLEASE ENTER THE WEEKEND NIGHTS IN THE BOOKING')
    wk = st.text_input('PLEASE ENTER THE WEEK NIGHTS IN THE BOOKING')
    park = (lambda x:1 if x == 'Yes' else 0)(st.selectbox('IS PARKING INCLUDED IN THE BOOKING', ['Yes', 'No']))
    month = st.slider('WHAT WILL BE THE MONTH OF ARRIVAL ?', min_value = 1, max_value = 12, step = 1)
    day = st.slider('WHAT WILL BE THE DAY OF ARRIVAL ?', min_value = 1, max_value = 31, step = 1)
    wkday_lambda = (lambda x:0 if x== 'MON' else 1 if x== 'TUE' else 2 if x== 'WED' else 3 if x== 'THU' 
                    else 4 if x== 'FRI' else 5 if x== 'SAT' else 6  )
    wkday = wkday_lambda(st.selectbox('WHAT IS THE WEEKDAY OF ARRIVAL ? ',['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']))



    tran_data = pt.transform([[lt, price]])
    lt_t = tran_data[0][0]
    price_t = tran_data[0][1]
    
    imp_list = [lt_t, mst, spcl, price_t, adult, wkd, wk, park, month, day, wkday]


    if st.button('PREDICT'):
        response = prediction(inp_list)
        st.success(response)

if __name__ == '__main__':
    main()
