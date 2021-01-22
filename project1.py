import streamlit as st
import pandas as pd
import numpy as np
import  plotly.express as px
#from wordcloud import wordcloud, STOPWORDS
#import matplotlib.pyplot as pltS


st.title("Validation of EDHW Contract loans Report")
st.sidebar.title("Validation of EDHW Contract loans Report")

st.markdown("This application is a Dashboard to analyze September reports on Contract loans ")
st.sidebar.markdown("This application is a Dashboard to analyze September reports on Contract loans ")

dataset_name = st.sidebar.selectbox("Choose the Month", (" ","January", "October","November","September"))


def get_dataset(dataset_name):
    if dataset_name == "January":
        data = "January_2020.csv"
    elif dataset_name == "September":
        data = "September_2020.csv"
    elif dataset_name == "November":
        data = "November_2020.csv"
    else:
        data = "October_2020.csv"
    return data

DATA_URL = get_dataset(dataset_name)

@st.cache(allow_output_mutation=True)
#@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data = load_data()

#'''Function of categorizing the Perfromance_class of customers'''
#data_performance = db
def performance_cat(x):
    if x == 0:
        return ("Normal loans")
    elif x > 0 and x <=3:
        return ("Watch loans")
    elif x >3 and x <= 6:
        return ("Substandard loans")
    elif x >6 and x <= 12:
        return ("Doubtful loans")
    elif x >12 and x <= 24:
        return ("Loss loans")
    else:
        return ("Writtern Off")

data['BSD_PERFORMANCE_DESC'] = data['INSTALMENTS_IN_ARREARS'].apply(performance_cat)


#'''Function of categorizing the Perfromance_class of customers after inspection'''
#data_performance = db
def Inspect_cat(x):
    if x == "Normal loans":
        return ("NL")
    elif x == "Watch loans":
        return ("WL")
    elif x == "Substandard loans":
        return ("SL")
    elif x =="Doubtful loans":
        return ("DL")
    elif x =="Loss loans":
        return ("LL")
    else:
        return ("WO")
data['BNR_PERFORMANCE_CLASS'] = data['BSD_PERFORMANCE_DESC'].apply(Inspect_cat)

comparison_column = np.where(data["PERFORMANCE_CLASS_DESC"] == data['BSD_PERFORMANCE_DESC'], True, False)
data["Inspection"] = comparison_column

#Plot Interactive Bar Plots and Pie Charts
#Add sidebar before introduce our widget
#'''Function of categorizing the banks'''
def banks_cat(x):
    if x == 10:
        return ("I&M bank")
    elif x ==11:
        return ("Ecobank")
    elif x == 15:
        return ("Access bank")
    elif x ==20:
        return ("AB bank")
    elif x == 30:
        return ("Cogebanque")
    elif x ==35:
        return ("NCBA")
    elif x == 40:
        return ("BK")
    elif x ==44:
        return ("BPR")
    elif x == 45:
        return ("Urwego bank")
    elif x ==50:
        return ("BRD")
    elif x == 60:
        return ("KCB")
    elif x == 70:
        return ("GT bank")
    elif x == 75:
        return ("Zigama Css")
    elif x == 76:
        return ("Bank of Africa")
    elif x == 80:
        return ("Unguka")
    else:
        return ("Equity bank")
data['Banks'] = data['LE_BOOK'].apply(banks_cat)

st.sidebar.markdown("### Amount of non performing Loans ")
#select = st.sidebar.selectbox('Visualisation type', [' ','Histogram', 'Pie chart'], key='1')
data.DISBURSED_AMOUNT=data['DISBURSED_AMOUNT'].astype(str).str.replace(',', '')
data['DISBURSED_AMOUNT'] = pd.to_numeric(data['DISBURSED_AMOUNT'], errors='coerce')
#creating new DataFrame for counting the computation

#Separating the Incorrect after supervison
incorrect = data.loc[data.Inspection == False]
amount_by_bank = incorrect.groupby('Banks')['DISBURSED_AMOUNT'].sum()
Total_amount = incorrect['DISBURSED_AMOUNT'].sum()

amount_by_bank = pd.DataFrame({'Banks':amount_by_bank.index, 'DISBURSED_AMOUNT':amount_by_bank.values})

fig = px.pie(amount_by_bank, values='DISBURSED_AMOUNT', names='Banks', title =( dataset_name+' '+"Disbursed amount"+' '+ "for non performed Loans"),
           color_discrete_sequence=px.colors.diverging.BrBG)
st.plotly_chart(fig, use_container_width=True)

st.markdown(" Bank's amount of Non performing loan")
if st.sidebar.checkbox("Show raw data", False, key='0'):
        st.write(amount_by_bank)

def Inspect_cat(x):
    if x == True:
        return ("performed loans")
    else:
        return ("Non performed loans")
data['PERFORMANCE'] = data['Inspection'].apply(Inspect_cat)
#creating new DataFrame for counting the computation
inspection_count = data['PERFORMANCE'].value_counts()
inspection_count = pd.DataFrame({'Inspection':inspection_count.index, 'performance':inspection_count.values})

#Plot Number of Inspection by banks performance for Each Airlines
st.sidebar.subheader("Breakdown banks contract Loans performance"+' '+"for"+' '+dataset_name)
choice = st.sidebar.multiselect("Pick Banks", (' ','I&M bank', 'Ecobank', 'Access bank', 'AB bank', 'Cogebanque','NCBA','BK','BPR','Urwego bank',
                                               'BRD', 'KCB', 'GT bank','Zigama Css','Bank of Africa','Unguka','Equity bank'), key='0')
st.subheader("Breakdown banks contract Loans performance"+' '+"for"+' '+ dataset_name)
if len(choice) > 0:
    choice_data = data[data.Banks.isin(choice)]
    fig_choice = px.histogram(choice_data, x='Banks', y='PERFORMANCE', histfunc='count', color='PERFORMANCE',
    facet_col = 'PERFORMANCE', labels={'PERFORMANCE':'performance'}, height=600, width=800)
    st.plotly_chart(fig_choice, use_container_width=True)

#Sum of money by banks
#
#st.write('{:,}'.format(Total_amount))

st.subheader("Contract Loan Amount by individual Bank")
st.sidebar.subheader("Banks Contract Loan amount")
bank = st.sidebar.radio("Select Bank", ( "Ecobank", "Access bank", "AB bank", "Cogebanque","Urwego bank",
                                               "BRD","NCBA","BK","BPR", "KCB", "GT bank","Zigama Css","Bank of Africa","Unguka","Equity bank"))
#creating new DataFrame for counting the computation
def get_data(bank):
    if bank == "Ecobank":
        df = data[data['LE_BOOK']== 11]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Access bank":
        df = data[data['LE_BOOK']== 15]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "AB bank":
        df = data[data['LE_BOOK']== 20]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Cogebanque":
        df = data[data['LE_BOOK']== 30]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Urwego bank":
        df = data[data['LE_BOOK']== 45]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "BRD":
        df = data[data['LE_BOOK']== 50]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "NCBA":
        df = data[data['LE_BOOK']== 35]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "BK":
        df = data[data['LE_BOOK']== 40]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "BK":
        df = data[data['LE_BOOK']== 40]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "BPR":
        df = data[data['LE_BOOK']== 44]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "KCB":
        df = data[data['LE_BOOK']== 60]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "GT bank":
        df = data[data['LE_BOOK']== 70]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Zigama Css":
        df = data[data['LE_BOOK']== 75]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Bank of Africa":
        df = data[data['LE_BOOK']== 76]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Unguka":
        df = data[data['LE_BOOK']== 80]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "Equity bank":
        df = data[data['LE_BOOK']== 85]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    elif bank == "I&M bank":
        df = data[data['LE_BOOK']== 10]
        df_t = df.groupby('PERFORMANCE')['DISBURSED_AMOUNT'].sum()
    return df_t

x_count = get_data(bank)
x_count = pd.DataFrame({'Inspection':x_count.index, 'performance':x_count.values})
fig = px.pie(x_count, values='performance', names='Inspection',title =(bank+' '+ 'loans performance indicator'+' '+"for"+' '+dataset_name),
                 color_discrete_sequence=px.colors.diverging.BrBG)
st.plotly_chart(fig, use_container_width=True)

st.markdown(bank +' '+"loan amount for"+' '+dataset_name)
if st.sidebar.checkbox("Show raw data", False, key='1'):
        st.write(x_count)
