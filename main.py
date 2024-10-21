# %% Libraries
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import numpy as np
from datetime import datetime
import datetime as dt
import calendar
import json
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules,fpgrowth
import networkx as nx
from PIL import Image


def main():
    im = Image.open('im1.png')
    # Set page config
    st.set_page_config(page_title="Market Basket Analysis",layout="wide",page_icon=im)

    # st. set_page_config(layout="wide")
    page = st.sidebar.radio("NAVIGATION PANEL:", ["Dashboard","Product Recommendation using apriori","Product Recommendation using fpgrowth ","Cart Recommendation"])
   
    #Add sidebar to the app
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("Made By:--")
    st.sidebar.markdown("Charan Thej")
    
    # Read clean dataset
    basket = pd.read_csv('mba.csv')   
    # First page
    if page == "Product Recommendation using apriori":
        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h2 style="color:white;text-align:center;">Product Recommendation using Market Basket Analysis</h2>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        st.markdown('### Analysis of the Data using apriori Rule')

        transactions=[]
        for item in basket['Member_number'].unique():
            lst=list(set(basket[basket['Member_number']==item]['itemDescription']))
            transactions.append(lst)
        te = TransactionEncoder()
        encodedData = te.fit(transactions).transform(transactions)
        data = pd.DataFrame(encodedData, columns=te.columns_)
        frequentItems= apriori(data, use_colnames=True, min_support=0.02)
        rules = association_rules(frequentItems, metric="lift", min_threshold=1)
        rules = rules.sort_values("lift",ascending=False).reset_index(drop= True)

        AgGrid(rules, theme='balham', height = 300, width = 20)

        product_catalog=basket["itemDescription"].unique()
        
        #### Need to have a drop down to choose country and then filter dataset based on that
        st.markdown('## Choose Product:')
        prod_option = st.selectbox('',product_catalog)

        st.write("Your Selected Item is:",prod_option)
        
        # Opening JSON file
        with open('item_sets.json') as json_file:
            data = json.load(json_file)
       
        # Display    
        if len(data[prod_option]) == 0 :
            st.error("Oops! No product recommendations available yet! Please select a different items.")
        else:
            st.markdown("####")
            st.success("##### People Also bought These products.")
            for d in data[prod_option]:
                if d:
                    st.markdown("- " + d)
    #%%
    if page == "Product Recommendation using fpgrowth ":
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h2 style="color:white;text-align:center;">Product Recommendation using Market Basket Analysis</h2>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        st.markdown('### Analysis of the Data using fpgrowth rule')
        transactions=[]
        for item in basket['Member_number'].unique():
            lst=list(set(basket[basket['Member_number']==item]['itemDescription']))
            transactions.append(lst)
        te = TransactionEncoder()
        encodedData = te.fit(transactions).transform(transactions)
        data1= pd.DataFrame(encodedData, columns=te.columns_)
        ft=fpgrowth(data1,use_colnames=True,min_support=0.02)
        rules1 = association_rules(ft, metric="confidence", min_threshold=0.2).iloc[:,:-3]
        rules1["antecedents_length"] = rules1["antecedents"].apply(lambda x: len(x))
        rules1["consequents_length"] = rules1["consequents"].apply(lambda x: len(x))
        rules1.sort_values("confidence")
        AgGrid(rules1, theme='balham', height = 300, width = 20)

        product_catalog=basket["itemDescription"].unique()
        
        #### Need to have a drop down to choose country and then filter dataset based on that
        st.markdown('## Choose Product:')
        prod_option = st.selectbox('',product_catalog)

        st.write("Your Selected Item is:",prod_option)
        
        # Opening JSON file
        with open('fitem_sets.json') as json_file:
            data1 = json.load(json_file)
       
        # Display    
        if len(data1[prod_option]) == 0 :
            st.error("Oops! No product recommendations available yet! Please select a different items.")
        else:
            st.markdown("####")
            st.success("##### People Also bought These products.")
            for d in data1[prod_option]:
                if d:
                    st.markdown("- " + d)
    #%%    
  
    if page == "Cart Recommendation":
        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h2 style="color:white;text-align:center;">Cart Recommendation</h2>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        product_catalog=basket["itemDescription"].unique()

        #Opening JSON file
        with open('fitem_sets.json') as json_file:
            data = json.load(json_file)
        
        #### Need to have a drop down to choose items and then filter dataset based on that
        st.markdown('## Add Items To cart to get Recommendations:')
        prod_option = st.multiselect('',product_catalog)

        st.write('You selected Items:', prod_option)

        st.success("##### People also bought these products...")

        unique=[]

        for key in prod_option:
            for x in data[key]:
                if x not in unique:
                    if x not in prod_option:
                        unique.append(x) 

        for d in unique:
            if d:
                st.markdown("- " + d)


    #%%
    if page == "Dashboard":

        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h2 style="color:white;text-align:center;">Statistical Analysis</h2>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        st.markdown('- Statistical analysis refers to the process of collecting, organizing, analyzing, interpreting, and presenting data in order to uncover patterns, trends, relationships, or insights within the data. It involves using various statistical methods and techniques to describe and summarize data, make inferences or predictions about populations or phenomena, and test hypotheses or research questions.')
        st.markdown('- Overall, statistical analysis provides a systematic and objective approach to understanding and making sense of data, which can inform decision-making, drive research, and contribute to knowledge in various fields.')
        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h4 style="color:white;text-align:center;">Most Sold items from the Data</h4>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        col1, col2, col3= st.columns([5, 1, 15])
        with col1:
            itemFrequency = basket['itemDescription'].value_counts().sort_values(ascending=False)
            itemFrequency
        with col3:
            fig1 = px.bar(itemFrequency.head(10), title='20 Most Frequent Items', color=itemFrequency.head(10), color_continuous_scale=px.colors.sequential.Mint)
            fig1.update_traces(texttemplate='%{y}', textposition='outside', hovertemplate = '<b>%{x}</b><br>No. of Transactions: %{y}')
            fig1.update_layout(showlegend=False,
                                        height=400, width = 750,
                                        margin={'t': 20, 'b': 0})
            st.plotly_chart(fig1)

        st.markdown('## Observations :-')
        st.markdown('- The above chart shows the items which are most sold from a retail shop.')
        st.markdown('- Whole Milk is the best-selling product by far, followed by other vegetables and rolls/buns.')
        st.markdown('- Whole Milk has More sales because milk is needed for every day.')

        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h4 style="color:white;text-align:center;">Dataset containing features of Day,Month and Year</h4>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")    
      
        dateTime=pd.to_datetime(basket['Date'])
        basket['Day']=dateTime.dt.day_name()
        basket['Month']=dateTime.dt.month_name()
        basket['Year']=dateTime.dt.year

        basket.drop('Date',axis=1,inplace=True)

        AgGrid(basket, theme='balham', height = 300, width = 150)

        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h4 style="color:black;text-align:center;">Most Sold items in a Day</h4>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")

        col1, col2, col3= st.columns([5, 1, 15])
        with col1:
            MostProductiveDay= basket.groupby('Day')['itemDescription'].count().sort_values(ascending=False)
            MostProductiveDay
        with col3:
            fig2 = px.bar(MostProductiveDay, title='Most Productive Day', color=MostProductiveDay, color_continuous_scale=px.colors.sequential.Mint)
            fig2.update_layout(margin=dict(t=50, b=0, l=0, r=0), titlefont=dict(size=20), xaxis_tickangle=0,coloraxis_showscale=False)
            fig2.update_traces(texttemplate='%{y}', textposition='outside', hovertemplate = '<b>%{x}</b><br>No. of Transactions: %{y}')
            st.plotly_chart(fig2)
        
        st.markdown('## Observations :-')
        st.markdown('- The chart represents more sales were happened in Thursday,Friday and Wednesday.')
        st.markdown('- These Sales were happened beacause more people used to buy in week days, they can peacefully go outing the weekends.')

        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h4 style="color:white;text-align:center;">Most Sold items in a Month</h4>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")
        



        col1, col2, col3= st.columns([5, 1, 15])
        with col1:
            MostProductiveMonth = basket.groupby('Month')['itemDescription'].count().sort_values(ascending=False)
            MostProductiveMonth
        with col3:
            fig3= px.bar(MostProductiveMonth, title='Most Productive Month', color=MostProductiveMonth, color_continuous_scale=px.colors.sequential.Mint)
            fig3.update_layout(margin=dict(t=50, b=0, l=0, r=0), titlefont=dict(size=20), xaxis_tickangle=0, coloraxis_showscale=False)
            fig3.update_traces(texttemplate='%{y}', textposition='outside', hovertemplate = '<b>%{x}</b><br>No. of Transactions: %{y}')
            st.plotly_chart(fig3)
        
        st.markdown('## Observations :-')
        st.markdown("- Highest sales has been noted during the Fall season, which are the month of August,May,January")
        st.markdown('- Lowest percentage of sales has been noted during the Winter season (September,December) where people are unable to leave the house due to harsh weather')
        

        # Title
        html_temp_title ="""<div style="background-color:#3498DB ;padding:2px">
            <h4 style="color:white;text-align:center;">Most Sold items in a Year</h4>
            </div>"""
        
        st.markdown(html_temp_title, unsafe_allow_html=True)
        st.markdown("")
        


        col1, col2, col3= st.columns([5, 1, 15])
        with col1:
            MostProductiveYear= basket.groupby('Year')['itemDescription'].count().sort_values(ascending=False)
            MostProductiveYear
        with col3:
            fig4 = px.bar(MostProductiveYear, title='Most Productive Year', color=MostProductiveYear, color_continuous_scale=px.colors.sequential.Mint)
            fig4.update_layout(margin=dict(t=50, b=0, l=0, r=0), titlefont=dict(size=20), xaxis_tickangle=0,coloraxis_showscale=False)
            fig4.update_traces(texttemplate='%{y}', textposition='outside', hovertemplate = '<b>%{x}</b><br>No. of Transactions: %{y}')
            st.plotly_chart(fig4)

        st.markdown('## Observations :-')
        st.markdown('- More Sales were happened inthe year 2015.')
        st.markdown('- From the above chart we should know that sales were increased from 2014 to 2015.')


        transactions=[]
        for item in basket['Member_number'].unique():
            lst=list(set(basket[basket['Member_number']==item]['itemDescription']))
            transactions.append(lst)
        te = TransactionEncoder()
        encodedData = te.fit(transactions).transform(transactions)
        data = pd.DataFrame(encodedData, columns=te.columns_)
        frequentItems= apriori(data, use_colnames=True, min_support=0.06)
        rules = association_rules(frequentItems, metric="lift", min_threshold=1)
        rules = rules.sort_values("lift",ascending=False).reset_index(drop= True)


        st.markdown("")


#%%
if __name__ == "__main__":
    main()