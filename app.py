import numpy as np
import streamlit as st
import pickle
import warnings
warnings.filterwarnings("ignore")
model = pickle.load(open("model_churn.sav","rb"))

def predict_status(age, month_income, gender, no_of_years, total_debit_transactions_s1,
                   total_debit_transactions_s2, total_debit_transactions_s3, total_debit_amount_s1,
                   total_debit_amount_s2, total_debit_amount_s3,
                   total_credit_transactions_s1, total_credit_transactions_s2, total_credit_transactions_s3,
                   total_credit_amount_s1, total_credit_amount_s2, total_credit_amount_s3, total_debit_amount,
                   total_debit_transactions, total_credit_amount, total_credit_transactions, total_transactions,
                   CUS_Target, TAR_Desc, married, other, partner, single, widowed):


    input_data = np.asarray([[age, month_income, gender, no_of_years, total_debit_transactions_s1,
                   total_debit_transactions_s2, total_debit_transactions_s3, total_debit_amount_s1,
                   total_debit_amount_s2, total_debit_amount_s3,
                   total_credit_transactions_s1, total_credit_transactions_s2, total_credit_transactions_s3,
                   total_credit_amount_s1, total_credit_amount_s2, total_credit_amount_s3, total_debit_amount,
                   total_debit_transactions, total_credit_amount, total_credit_transactions, total_transactions,
                   CUS_Target, TAR_Desc, married, other, partner, single, widowed]])
    prediction = model.predict(input_data)
    return prediction[0]

def main():
    st.title("BANK CHURN PREDICTION")
    age = st.text_input("Enter the Age")
    month_income = st.text_input("Enter the Month income")
    gender = st.text_input("Enter the Gender")
    no_of_years = st.text_input("Enter the Total number of years completed with bank")
    total_debit_transactions_s1 = st.text_input("Enter the Total debit transactions for Quater 1")
    total_debit_transactions_s2 = st.text_input("Enter the Total debit transactions for Quater 2")
    total_debit_transactions_s3 = st.text_input("Enter the Total debit transactions for Quater 3")
    total_debit_amount_s1 = st.text_input("Enter the Total debit amount for Quater 1")
    total_debit_amount_s2 = st.text_input("Enter the Total debit amount for Quater 2")
    total_debit_amount_s3 = st.text_input("Enter the Total debit amount for Quater 3")
    total_credit_transactions_s1 = st.text_input("Enter the Total credit transactions for Quater 1")
    total_credit_transactions_s2 = st.text_input("Enter the Total credit transactions for Quater 2")
    total_credit_transactions_s3 = st.text_input("Enter the Total credit transactions for Quater 3")
    total_credit_amount_s1 = st.text_input("Enter the Total credit amount for Quater 1")
    total_credit_amount_s2 = st.text_input("Enter the Total credit amount for Quater 2")
    total_credit_amount_s3 = st.text_input("Enter the Total credit amount for Quater 3")
    total_debit_amount = st.text_input("Enter the Total debit amount")
    total_debit_transactions = st.text_input("Enter the Total debit transactions")
    total_credit_amount = st.text_input("Enter the Total credit amount")
    total_credit_transactions = st.text_input("Enter the Total credit transactions")
    total_transactions = st.text_input("Enter the Total transactions")
    CUS_Target = st.text_input("Enter the Customer target")
    TAR_Desc = st.text_input("Enter the Target description")
    married = st.text_input("Enter the Customer is married or not")
    other = st.text_input("Enter the Customer is other or not")
    partner = st.text_input("Enter the Customer is having partner or not")
    single = st.text_input("Enter the Customer is single or not")
    widowed = st.text_input("Enter the Customer is widowed or not")


    result = ''
    if st.button("Predict"):
        diagnosis = predict_status(age, month_income, gender, no_of_years, total_debit_transactions_s1,
                   total_debit_transactions_s2, total_debit_transactions_s3, total_debit_amount_s1,
                   total_debit_amount_s2, total_debit_amount_s3,
                   total_credit_transactions_s1, total_credit_transactions_s2, total_credit_transactions_s3,
                   total_credit_amount_s1, total_credit_amount_s2, total_credit_amount_s3, total_debit_amount,
                   total_debit_transactions, total_credit_amount, total_credit_transactions, total_transactions,
                   CUS_Target, TAR_Desc, married, other, partner, single, widowed)

        if result == "1":
            st.info("Churn Account")


        else:
            st.success("Active Account")


if __name__=="__main__":
    main()


