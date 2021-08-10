########## Libraries
from time import strftime
import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(layout="centered")
import openpyxl
from datetime import datetime, date
import base64 
import time

########### Frontend
def main():
    username= st.sidebar.text_input('Username', value='John Doe')
    password= st.sidebar.text_input('Password', value='A123', type="password")
    privilege = st.sidebar.text_input('Resource', value='Entry')
    employee_list = pd.read_excel("EmployeeList.xlsx", engine="openpyxl", index_col=0)
    employee_list['USERNAME'] = employee_list['Level'].astype(str)+'_'+employee_list['Name'].astype(str)
    employee_list['USERNAME'] = employee_list['USERNAME'].str.strip().str.replace(' ', '')
    employee_list['USERNAME'] = employee_list['USERNAME'].str.lower()
    up_key = str(privilege)[0]+'_'+str(username)
    up_key = up_key.replace(' ', '')
    up_key = up_key.lower()
    if (str(username) in employee_list['Name'].tolist()) and (str(password) in employee_list['PASSWORD'].astype(str).tolist()):
        if (up_key[0] == 'a') and (up_key in employee_list['USERNAME'].tolist()):
            resource1 = st.selectbox("Resource", options=["Analysis", "Changes"])
            if resource1 == "Analysis":
                st.title(resource1)
                st.sidebar.subheader("Successful Login!")
                analysis_results = pd.read_excel("Results.xlsx", engine="openpyxl", index_col=0)
                analysis_results['Chargeable Amount'] = analysis_results['Hours']* analysis_results['Charge']
                analysis_results = analysis_results[['Name', 'Company', 'Division', 'Year of Work','Start Time', 'End Time', 'Date', 'Hours', 'Charge', 'Chargeable Amount', 'Description']]
                st.subheader("All Entries")
                st.dataframe(analysis_results.tail())
                csv_downloader(analysis_results)
                st.subheader("Filter")
                for i in range(1):
                    cols = st.columns(3)
                    filter1 = cols[0].selectbox("Filter 1", options=['None', 'Date','Name', 'Company', 'Division', 'Year of Work'] )
                    if filter1 == "Date":
                        condition_options = analysis_results[str(filter1)].unique()
                        condition1 = cols[1].selectbox("Condition 1", options=condition_options)
                        analysis_results = analysis_results[analysis_results[str(filter1)]==str(condition1)]
                    elif filter1 == "None":
                        condition_options = ["None"]
                        condition1 = cols[1].selectbox("Condition 1", options=condition_options)
                    else:
                        condition_options = analysis_results[str(filter1)].unique()
                        condition1 = cols[1].selectbox("Condition 1", options=condition_options)
                        analysis_results = analysis_results[analysis_results[str(filter1)]==str(condition1)]
                st.subheader("Pivot Table")
                for i in range(1):
                    cols = st.columns(3)
                    row_ = cols[0].multiselect("Rows", options=['Name', 'Company', 'Division', 'Date', 'Year of Work'])
                    col_ = cols[1].multiselect("Columns", options=['Name', 'Company', 'Division', 'Date', 'Year of Work'] )
                    value_ = cols[2].multiselect("Values", options=['Hours', 'Charge', 'Chargeable Amount'])
                if len(col_)==0 or len(row_)==0 or len==(value_)==0:
                    pass
                else:
                    temp = pd.pivot_table(analysis_results, index=row_, columns=col_, values=value_, aggfunc='sum', fill_value=0)
                    st.dataframe(temp)
                    csv_downloader(temp)
            if resource1 == "Changes":
                st.title(resource1)
                change = st.selectbox("Change", options=["Employees", "Companies"])
                if change == "Employees":
                    df1 = pd.read_excel("EmployeeList.xlsx", engine="openpyxl", index_col=0)
                    st.table(df1)
                    st.subheader("Instructions:")
                    st.write("* Add Employee details as above seperated by commas for Addition")
                    st.write("* Add Name of Employee as listed in the above table for Deletion")
                    st.subheader("Example:")
                    st.write("Barrack Obama, A, Freedom123, 4000")
                    ad1 = st.selectbox("Add or Delete Employee", options=["","Add", "Delete"])
                    if ad1 == "Add":
                        add1 = st.text_input("Information to Add")
                        if st.text_input("Admin Key", type="password") == "3.141592654":
                            value_add = str(add1).split(",")
                            df1 = df1.append({
                                "Name": value_add[0],
                                "Level": value_add[1],
                                "PASSWORD": value_add[2],
                                "Charge": value_add[3]
                            }, ignore_index=True)
                            df1.to_excel("EmployeeList.xlsx", engine="openpyxl")
                    elif ad1 == "Delete":
                        del1 = st.text_input("Name to Delete")
                        if st.text_input("Admin Key", type="password") == "3.141592654":
                            df1 = df1[df1["Name"]!=str(del1)]
                            df1.to_excel("EmployeeList.xlsx", engine="openpyxl")
                if change == "Companies":
                    df2 = pd.read_excel("ClientList.xlsx", engine="openpyxl", index_col=0)
                    st.table(df2)
                    st.subheader("Instructions:")
                    st.write("* Add Company Name for Addition/ Deletion")
                    st.subheader("Example:")
                    st.write("Apple")
                    ad2 = st.selectbox("Add or Delete Company", options=["","Add", "Delete"])
                    if ad2 == "Add":
                        add2 = st.text_input("Company")
                        if st.text_input("Admin Key", type="password") == "3.141592654":
                            df2 = df2.append({
                                "Company": add2}, ignore_index=True)
                            df2.to_excel("ClientList.xlsx", engine="openpyxl")
                    elif ad2 == "Delete":
                        del2 = st.text_input("Name to Delete")
                        if st.text_input("Admin Key", type="password") == "3.141592654":
                            df2 = df2[df2["Company"]!=str(del2)]
                            df2.to_excel("ClientList.xlsx", engine="openpyxl")    
        elif (up_key[0] == 'e') and (up_key in employee_list['USERNAME'].tolist()):
            st.sidebar.subheader("Successful Login!")
            resource = st.selectbox("Resource", options=["Timesheet Entry", "History & Correction"])
            if resource=="Timesheet Entry":
                with st.form(key="Initial Information"):
                    st.title(resource)
                    client_list = pd.read_excel("ClientList.xlsx", engine="openpyxl", index_col=0)
                    client = client_list["Company"].tolist()
                    workdiv_ = st.selectbox("Work Division", options=["Accounting", "Auditing", "Company Secretarial", "Tax", "Other", "Office"])
                    company_ = st.selectbox("Name of Company", options=client)
                    year_of_work_ = st.selectbox("Year of Work", options=["2018", "2019", "2020", "2021", "Other"])
                    description_ = st.text_area("Description", value="")
                    for i in range(1):
                        cols = st.columns(2)
                        start_ = cols[0].time_input("Start")
                        end_ =cols[1].time_input("End")
                        seconds = (datetime.combine(date.min, end_) - datetime.combine(date.min, start_)).seconds
                        minutes_ = (seconds//60)%60
                    today_ = datetime.today() 
                    date_ = st.date_input("Date Worked", value=today_)
                    totaltime_ = float(round((minutes_/60),2))
                    st.form_submit_button("Review")
                with st.form(key="Review"):
                    if datetime.combine(date_, datetime.min.time()) <= today_:
                        st.write("Name: "+str(username))
                        st.write("Division: "+str(workdiv_))
                        st.write("Company: "+str(company_))
                        st.write("Year of Work: "+str(year_of_work_))
                        st.write("Description: "+str(description_))
                        st.write("Start Time: "+str(start_))
                        st.write("End Time: "+str(end_))
                        st.write("Date: "+str(date_))  
                    if (st.form_submit_button("Submit")) and (datetime.combine(date_, datetime.min.time()) <= today_):
                        results = pd.read_excel("Results.xlsx", engine="openpyxl", index_col=0)
                        charge_ = employee_list.loc[employee_list['Name']==str(username)]
                        charge_ = int(charge_['Charge'])
                        results = results.append({"Key":str(datetime.now().strftime("%H:%M:%S"))+"_"+str(up_key),
                                                "Name":str(username),
                                                "Company":str(company_),
                                                "Division":str(workdiv_),
                                                "Year of Work":str(year_of_work_),
                                                "Description":str(description_),
                                                "Date": str(date_),
                                                "Start Time": str(start_),
                                                "End Time": str(end_),
                                                "Hours":float(totaltime_),
                                                "Charge":float(charge_)}, ignore_index=True)
                        results.to_excel("Results.xlsx")
                    else:
                        pass
            elif resource=="History & Correction":
                st.title(resource)
                display_results = pd.read_excel("Results.xlsx", engine="openpyxl")
                display_results = display_results[['Name', 'Company', 'Division', 'Year of Work','Start Time', 'End Time', 'Date', 'Description']]
                display_results = display_results[display_results['Name']==str(username)]
                st.dataframe(display_results)
    else:
        st.sidebar.subheader('Unsuccessful Login!')

############### FUNCTIONS
def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    timestr = time.strftime("%Y%m%d_%H%M%S")
    new_filename = "{}.csv".format(timestr)
    # st.markdown("#### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Download as CSV</a>'
    st.markdown(href,unsafe_allow_html=True)

@st.cache
def load_data():
    return 

if __name__ == "__main__":
    main()
