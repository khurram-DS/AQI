import streamlit as st
# Eda packages

import pandas as pd
import numpy as np

#Data viz packages

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

#function

def main():
    
    title_container1 = st.container()
    col1, col2 ,  = st.columns([6,12])
    from PIL import Image
    image = Image.open('static/asia.jpeg')
    with title_container1:
        with col1:
            st.image(image, width=200)
        with col2:
            st.markdown('<h1 style="color: tomato;">ASIA Consulting</h1>',
                           unsafe_allow_html=True)
    
    st.subheader('Air pollution Kuwait project')
    
    st.sidebar.image("static/AQI.jpg", use_column_width=True)
    activites = ["About","Data interpretation","AQI calculation","Station wise Data","Data Anlaysis"]
    choice =st.sidebar.selectbox("Select Activity",activites)
    @st.cache(allow_output_mutation=True)
    def get_df(file):
      # get extension and read file
      extension = file.name.split('.')[1]
      if extension.upper() == 'CSV':
        df = pd.read_csv(file,parse_dates = ["Date and Time"],error_bad_lines=False)
      elif extension.upper() == 'XLSX':
        df = pd.read_excel(file,parse_dates = ["Date and Time"],error_bad_lines=False)
      
      return df
    file = st.file_uploader("Upload file", type=['csv' 
                                             ,'xlsx'])
    if not file:
        st.write("Upload a .csv or .xlsx file to get started")
        return
      
    df = get_df(file)
    
    st.write("**Data has been loaded Successfully**")
    df['year'] = pd.DatetimeIndex(df['Date and Time']).year
    da=df.loc[df['year'] == 2017]
    da = da.replace([2017],2018)
    ps = pd.Series(da["Date and Time"])
    da["Date and Time"] = ps.apply(lambda dt: dt.replace(year=2018))
    aa=pd.concat([df, da]).sort_values(by="Date and Time")
    
    eight=aa.loc[aa['year'] == 2018]
    ds=aa.copy()
    #lets fill the null value with mean value of the column data as per the date.
    col= ['CO','NO','NO2','NOx','O3','PM10','SO2']
    from sklearn.impute import SimpleImputer
    imp=SimpleImputer(strategy='mean')
    for i in col:
        ds[i]=imp.fit_transform(ds[i].values.reshape(-1,1))
    #aqi
    da=ds.copy()
    da.sort_values(["Station", "Date and Time"], inplace = True)
    da["PM10_24hr_avg"] = da.groupby("Station")["PM10"].rolling(window = 24, min_perioda = 16).mean().values
    da["SO2_24hr_avg"] = da.groupby("Station")["SO2"].rolling(window = 24, min_perioda = 16).mean().values
    da["NOx_24hr_avg"] = da.groupby("Station")["NOx"].rolling(window = 24, min_perioda = 16).mean().values
    da["NO2_1hr_avg"] = da.groupby("Station")["NO2"].rolling(window = 1, min_perioda = 1).mean().values
    da["CO_8hr_max"] = da.groupby("Station")["CO"].rolling(window = 8, min_perioda = 1).max().values
    da["O3_8hr_max"] = da.groupby("Station")["O3"].rolling(window = 8, min_perioda = 1).max().values
    
    dsub=da.copy()
    
    def get_PM10_subindex(x):
        if x <= 54:
            return 0 + (x - 0)* 50/54
        elif x <= 154:
            return 51 + (x-55)* 49/99
        elif x <= 254:
            return 101 + (x - 155) * 49 / 99
        elif x <= 354:
            return 151 + (x - 255) * 49/99
        elif x <= 424:
            return 201 + (x - 355) * 99 / 69
        elif x > 424:
            return 301 + (x - 425) * 199 / 179
        else:
            return 0
                
    dsub["PM10_AQI"] = dsub["PM10_24hr_avg"].apply(lambda x: get_PM10_subindex(x))
    
    ## SO2 Sub-Index calculation
    def get_SO2_subindex(x):
        if x <= 35:
            return 0 + (x - 0)* 50/35
        elif x <= 75:
            return 51 + (x-36)* 49/39
        elif x <= 185:
            return 101 + (x - 76) * 49 / 109
        elif x <= 304:
            return 151 + (x - 186) * 49/118
        elif x <= 604:
            return 201 + (x - 305) * 99 / 299
        elif x > 604:
            return 301 + (x - 605) * 199 / 399
        else:
            return 0
            
    dsub["SO2_AQI"] = dsub["SO2_24hr_avg"].apply(lambda x: get_SO2_subindex(x))
    
    
     ## NOx Sub-Index calculation
    def get_NOx_subindex(x):
        if x <= 40:
            return x * 50 / 40
        elif x <= 80:
            return 50 + (x - 40) * 50 / 40
        elif x <= 180:
            return 100 + (x - 80) * 100 / 100
        elif x <= 280:
            return 200 + (x - 180) * 100 / 100
        elif x <= 400:
            return 300 + (x - 280) * 100 / 120
        elif x > 400:
            return 400 + (x - 400) * 100 / 120
        else:
            return 0
            
    dsub["NOx_AQI"] = dsub["NOx_24hr_avg"].apply(lambda x: get_NOx_subindex(x))
            ## NO2 Sub-Index calculation
    def get_NO2_subindex(x):
        if x <= 53:
            return 0 + (x - 0)* 50/53
        elif x <= 100:
            return 51 + (x-54)* 49/46
        elif x <= 360:
            return 101 + (x - 101) * 49 / 259
        elif x <= 649:
            return 151 + (x - 361) * 49/288
        elif x <= 1249:
            return 201 + (x - 650) * 99 / 599
        elif x > 1249:
            return 301 + (x - 1250) * 199 / 799
        else:
            return 0
            
    dsub["NO2_AQI"] = dsub["NO2_1hr_avg"].apply(lambda x: get_NO2_subindex(x))
            ## CO Sub-Index calculation
    def get_CO_subindex(x):
        if x <= 4.4:
            return 0 + (x - 0)* 50/4.4
        elif x <= 9.4:
            return 51 + (x-4.5)* 49/4.9
        elif x <= 12.4:
            return 101 + (x - 9.5) * 49 / 2.9
        elif x <= 15.4:
            return 151 + (x - 12.5) * 49/2.9
        elif x <= 30.4:
            return 201 + (x - 15.5) * 99 / 14.9
        elif x > 30.4:
            return 301 + (x - 30.5) * 199 / 19.9
        else:
            return 0
            
            
    dsub["CO_AQI"] = dsub["CO_8hr_max"].apply(lambda x: get_CO_subindex(x))
            ## O3 Sub-Index calculation
    def get_O3_subindex(x):
        if x <= 54:
            return 0 + (x - 0)* 50/54
        elif x <= 70:
            return 51 + (x-55)* 49/15
        elif x <= 85:
            return 101 + (x - 71) * 49 / 14
        elif x <= 105:
            return 151 + (x - 86) * 49/19
        elif x > 200:
            return 301 + (x - 106) * 199 / 94
        else:
            return 0
            
    dsub["O3_AQI"] = dsub["O3_8hr_max"].apply(lambda x: get_O3_subindex(x))
            ## AQI bucketing
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x <= 100:
            return "Satisfactory"
        elif x <= 200:
            return "Moderate"
        elif x <= 300:
            return "Poor"
        elif x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return np.NaN
            
    dsub["Checks"] =(dsub["PM10_AQI"] > 0).astype(int) + \
                    (dsub["SO2_AQI"] > 0).astype(int) + \
                    (dsub["NOx_AQI"] > 0).astype(int) + \
                    (dsub["NO2_AQI"] > 0).astype(int) + \
                    (dsub["CO_AQI"] > 0).astype(int) + \
                    (dsub["O3_AQI"] > 0).astype(int)
                            
    dsub["Combined_AQI"] = round(dsub[[ "PM10_AQI", "SO2_AQI", "NOx_AQI","NO2_AQI","CO_AQI", "O3_AQI"]].max(axis = 1))
    dsub.loc[dsub["PM10_AQI"] <= 0, "Combined_AQI"] = np.NaN
    dsub.loc[dsub.Checks < 3, "Combined_AQI"] = np.NaN
    dsub["AQI_bucket_calculated"] = dsub["Combined_AQI"].apply(lambda x: get_AQI_bucket(x))
    dsub = dsub.dropna(how='any',axis=0)
            
    
    #station wise
    station1=dsub.loc[dsub['Station'] == 'ST1'].reset_index(drop=True)
    station2=dsub.loc[dsub['Station'] == 'ST2'].reset_index(drop=True)
    station3=dsub.loc[dsub['Station'] == 'ST3'].reset_index(drop=True)
    station4=dsub.loc[dsub['Station'] == 'ST4'].reset_index(drop=True)
    station5=dsub.loc[dsub['Station'] == 'ST5'].reset_index(drop=True)
    station6=dsub.loc[dsub['Station'] == 'ST6'].reset_index(drop=True)
    station7=dsub.loc[dsub['Station'] == 'ST7'].reset_index(drop=True)
    station8=dsub.loc[dsub['Station'] == 'ST8'].reset_index(drop=True)
    station9=dsub.loc[dsub['Station'] == 'ST9'].reset_index(drop=True)
    
    s1=station1.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s1['Station']='ST1'
                
                #staion2
    s2=station2.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s2['Station']='ST2'
                
                #staion3
    s3=station3.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s3['Station']='ST3'
                
                #staion4
    s4=station4.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s4['Station']='ST4'
                
                #station5
    s5=station5.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s5['Station']='ST5'
                
                #staion6
    s6=station6.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s6['Station']='ST6'
                
                #staion7
    s7=station7.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s7['Station']='ST7'
                
                #staion8
    s8=station8.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s8['Station']='ST8'
                
                #staion4
    s9=station9.groupby(pd.Grouper(key='Date and Time',freq='1D')).mean()
    s9['Station']='ST9'    
    
    frames=[s1,s2,s3,s4,s5,s6,s7,s8,s9]
    Average_day=pd.concat(frames).reset_index()
    Average_day['Date and Time']=Average_day['Date and Time'].dt.strftime('%d/%m/%Y')
    Average_day.rename(columns={'Date and Time':'Date'},inplace=True)
    ## AQI bucketing
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x <= 100:
            return "Satisfactory"
        elif x <= 200:
            return "Moderate"
        elif x <= 300:
            return "Poor"
        elif x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return np.NaN
    Average_day["Combined_AQI"] = round(Average_day[[ "PM10_AQI", "SO2_AQI", "NOx_AQI","NO2_AQI",
                                  "CO_AQI", "O3_AQI"]].max(axis = 1))
    Average_day.loc[Average_day["PM10_AQI"] <= 0, "Combined_AQI"] = np.NaN
    Average_day.loc[Average_day.Checks < 3, "Combined_AQI"] = np.NaN

    Average_day["AQI_bucket_calculated"] = Average_day["Combined_AQI"].apply(lambda x: get_AQI_bucket(x))
    # rearranging the column names
    Average_day = Average_day.dropna(how='any',axis=0)
    column_names = ['Date','Station','CO', 'NO', 'NO2', 'NOx', 'O3', 'PM10', 'SO2', 'PM10_24hr_avg','SO2_24hr_avg', 'NOx_24hr_avg', 'NO2_1hr_avg', 'CO_8hr_max','O3_8hr_max', 'PM10_AQI', 'SO2_AQI', 'NOx_AQI','NO2_AQI', 'CO_AQI', 'O3_AQI', 'Checks','Combined_AQI','AQI_bucket_calculated']
    Average_day = Average_day.reindex(columns=column_names)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    if choice == "About":
        
        st.subheader("""  ❓ So you must have thought that what is AQI, and why its so important or how it is impacting Human life's.""")
        st.markdown("""**Que1: What is AQI **""")
                    
        st.text("""
                
        The air quality index (AQI) is an index for reporting air quality on a daily basis. 
        It is a measure of how air pollution affects one's health within 
        a short time period. The purpose of the AQI is to help people know 
        how the local air quality impacts their health. 
        The Environmental Protection Agency (EPA) calculates the AQI for 
        five major air pollutants, for which national air quality standards 
        have been established to safeguard public health.

                1. Ground-level ozone
                2. Particle pollution/particulate matter (PM2.5/pm 10)
                3. Carbon Monoxide
                4. Sulfur dioxide
                5. Nitrogen dioxide

        The higher the AQI value, the greater the level of air pollution and the greater 
        the health concerns. The concept of AQI has been widely used in many developed
        countries for over the last three decades. AQI quickly disseminates air quality 
        information in real-time.""")
        st.markdown("""**Que2: How AQI is impacting Human Life's. **""")
        
        st.text("""Awareness of daily levels of air pollution is important,especially for 
those suffering from illnesses caused by exposure to air pollution.""")
        
        st.markdown(""" **🤔 Objectives of Fiinding Air Quality Index (AQI)**""")
        
        st.text("""
       - Comparing air quality conditions at different locations/cities.
    
       - It also helps in identifying faulty standards and inadequate monitoring programmes.
    
       - AQI helps in analysing the change in air quality (improvement or degradation).
    
       - AQI informs the public about environmental conditions. It is especially useful
         for people suffering from illnesses aggravated or caused by air pollution.""")
        
        st.markdown(""" **🤔 Who is most at risk from air pollution?**""")
        
        st.text("""
   — People with lung diseases, such as asthma, chronic bronchitis, and emphysema

   — Children, including teenagers

   — Active people of all ages who exercise or work extensively outdoors

   — Some healthy people are more sensitive to ozone""")
        
        
        from PIL import Image
        image = Image.open('static/kuwait.jpg')

        st.image(image, caption="Kuwait City air quality 'unhealthy' - Kuwait Times",width=600)
        st.text('© ASIA Consulting 2022')
        
    elif choice == "Data interpretation":
        st.subheader("Data Interpretation")
        from PIL import Image
        image = Image.open('static/raw.jpg')

        st.image(image, caption="Raw Data Interpretation",width=650)
        
        if st.checkbox('Show Raw Data Information'):
            st.subheader('Raw Data')
            st.write(df.head())
            
            st.markdown("""**Features Details(Column Details)**""")
            
            st.text("""
     1. Station - Station stands for number of stations these data Belongs to. 
     2. Date and Time - It gives the DEtails of Date and time the Data has been recorded.
     3. CO - CO stands for ( carbon monoxide measured in mg / m3 (milligrams per cubic meter of air))
     4. NO - Nitric oxide ( measured in FENO (fractional exhaled nitric oxide))
     5. NO2- Nitrogen dioxide (  measured in parts per billion (ppb) or (µg m-3))
     6. NOx- Any Nitric x-oxide (NOx is measured in ppb (parts per billion)
     7. O3- Ozone or Trioxygen ( O3 is measured in ug / m3 (micrograms per cubic meter of air)
     8. PM10- Particulate Matter 10-micrometer ( PM10 is measured in ug / m3 (micrograms per cubic meter of air)
     9. SO2- Sulphur Dioxide( SO2 is measured in ug / m3 (micrograms per cubic meter of air)""")
    
            st.subheader("""**Shape of the Data**""")
            st.subheader("we have total {} rows with {} columns".format(df.shape[0],df.shape[1]))
        
        if st.checkbox('Show Summary statistics'):
            
            st.subheader('Summary statistics')
            stat=df.describe().T
            st.write(stat)
            st.download_button(label='Download CSV',data=stat.to_csv(),mime='text/csv')
            st.markdown("""** 🧐 Observation: **
            
    1. we can observe the count value in table, there is large diffrence comparing 
       in every features so we can say that our data consist of NUll values.
    2. The standard deviation of PM10 quite high so we can conclude intially 
       that PM10 feature must contain some outliers.""")
            
            st.markdown("""** 🔍 How much data is been fine for PM10 without outliers **""")
            st.write('Minimum Data of PM10 is   :',df['PM10'].min())
            st.write('To 98% is considerable :',df['PM10'].quantile(.98))
            
            st.markdown("""**🧐 Observation: **
                        
    1. we Can say that my 98% of 'PM10' data is fine but still it's need to be taken care.
    2. so only 2% of PM10 Data is been corrupted""")
            
            st.markdown("""** 🔍 Lets find the time span of Data what we have loaded**""")
            
            st.write("The Air pollution data has been recorded from [{}] till date [{}] ".format(df['Date and Time'].min(),df['Date and Time'].max()))
        
        if st.checkbox('Data cleaning / interpretation'):
            st.markdown("""**🔍 Lets Find out the null value and its percentage with its impact on our Data set**""")
            # Missing values
            def missing_values_table(df):
                    # Total missing values
                    mis_val = df.isnull().sum()
                    
                    # Percentage of missing values
                    mis_val_percent = 100 * df.isnull().sum() / len(df)
                    
                    # Make a table with the results
                    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
                    
                    # Rename the columns
                    mis_val_table_ren_columns = mis_val_table.rename(
                    columns = {0 : 'Missing Values', 1 : '% of Total Values'})
                    
                    # Sort the table by percentage of missing descending
                    mis_val_table_ren_columns = mis_val_table_ren_columns[
                        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
                    '% of Total Values', ascending=False).round(1)
                    
                    # Print some summary information
                    st.write("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
                        "There are " + str(mis_val_table_ren_columns.shape[0]) +
                          " columns that have missing values.")
                    
                    # Return the dataframe with missing information
                    return mis_val_table_ren_columns
            
            missing_values= missing_values_table(df)
            st.write(missing_values.style.background_gradient(cmap='Reds'))
            st.markdown("""**🧐 Observation:** 
                        
    1. We can clearly observe that the Nox pollutant is having highest 40% NULL value. 
    
    2. CO pollutant is having least i.e 6% of NULL value present """)
            #df.drop(['date'],inplace=True,axis=1)
            
            st.markdown("""** we have noticed that we dont have Data for the year 2018**""")
            
            st.write(df.loc[df['year'] == 2018])
            
            
            if st.checkbox("💡 Let's predict 2018 Data"):                
                st.markdown("""** ✌️ we got the Data for the year 2018**""")
                st.write(eight.head())
                st.download_button(label='Download CSV',data=eight.to_csv(),mime='text/csv')
                
                
                st.markdown("""**🔍 Lets Find out the null value and its percentage with its impact on our Data set Again**""")
                 # Missing values
                def missing_values_table(aa):
                        # Total missing values
                        mis_val = aa.isnull().sum()
                        
                        # Percentage of missing values
                        mis_val_percent = 100 * aa.isnull().sum() / len(aa)
                        
                        # Make a table with the results
                        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
                        
                        # Rename the columns
                        mis_val_table_ren_columns = mis_val_table.rename(
                        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
                        
                        # Sort the table by percentage of missing descending
                        mis_val_table_ren_columns = mis_val_table_ren_columns[
                            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
                        '% of Total Values', ascending=False).round(1)
                        
                        # Print some summary information
                        st.write("Your selected dataframe has " + str(aa.shape[1]) + " columns.\n"      
                            "There are " + str(mis_val_table_ren_columns.shape[0]) +
                              " columns that have missing values.")
                        
                        # Return the dataframe with missing information
                        return mis_val_table_ren_columns
                
                missing_values= missing_values_table(aa)
                st.write(missing_values.style.background_gradient(cmap='Greens'))
                st.markdown("""**🧐 Observation:** 
                            
    1. We can clearly observe that the Nox pollutant is having highest 45% NULL value. 
    
    2. CO pollutant is having least i.e 6% of NULL value present """)
              
                st.markdown("""**🕵 Lets find the missing value**""")
            
            if st.checkbox("Impute Missing value"):
                
                st.markdown("""**Lets fill the missing value with the Average value of that particular column**""")
                
                title_container1 = st.container()
                col1, col2 ,  = st.columns([6,12])
                from PIL import Image
                #image = Image.open('static/asia.jpeg')
                with title_container1:
                    with col2:
                        st.image('https://i.pinimg.com/originals/4a/34/99/4a3499c6b5cca368ec4e3717f9077114.gif', width=300,caption='Imputing missing value')
                        
                
                st.markdown("""**🔍 Lets check whether we have succesfully imputed the missing values**""")
                # Missing values
                def missing_values_table(ds):
                        # Total missing values
                        mis_val = ds.isnull().sum()
                        
                        # Percentage of missing values
                        mis_val_percent = 100 * ds.isnull().sum() / len(ds)
                        
                        # Make a table with the results
                        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
                        
                        # Rename the columns
                        mis_val_table_ren_columns = mis_val_table.rename(
                        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
                        
                        # Sort the table by percentage of missing descending
                        mis_val_table_ren_columns = mis_val_table_ren_columns[
                            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
                        '% of Total Values', ascending=False).round(1)
                        
                        # Print some summary information
                        st.write("Your selected dataframe has " + str(ds.shape[1]) + " columns.\n"      
                            "There are " + str(mis_val_table_ren_columns.shape[0]) +
                              " columns that have missing values.")
                        
                        # Return the dataframe with missing information
                        return mis_val_table_ren_columns
                
                missing_values= missing_values_table(ds)
                st.write(missing_values.style.background_gradient(cmap='Greens'))
                cleaned_data=ds.copy()
                st.markdown("""**Download the cleaned Data for Future Reference**""")
                import base64
                import io
                towrite = io.BytesIO()
                downloaded_file = cleaned_data.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
                towrite.seek(0)  # reset pointer
                b64 = base64.b64encode(towrite.read()).decode() 
                linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="cleaned_data.csv">Download csv file</a>'
                st.markdown(linko, unsafe_allow_html=True)
    
                st.markdown("""**✌️✌️✌️ We got the cleaned Data let start doing our Analysis**""")
                st.text("© ASIA Consulting 2022")
        
    elif choice == "AQI calculation":
        
        
        from PIL import Image
        image = Image.open('static/formula.png')

        st.image(image, caption="AQI calculation",width=600)
        st.text("""
- The AQI calculation uses 7 measures: PM2.5, PM10, SO2, NOx, NH3, CO and O3.

- For PM2.5, PM10, SO2, NOx and NH3 the average value in last 24-hrs is used with the condition of having at least 16 values.

- For CO and O3 the maximum value in last 8-hrs is used.

- Each measure is converted into a Sub-Index based on pre-defined groups.

- Sometimes measures are not available due to lack of measuring or lack of required data points.

- Final AQI is the maximum Sub-Index with the condition that at least one of PM2.5 and PM10 should be available and at least 
  three out of the seven should be available.""")
        
            
        if st.checkbox("show the average hourly data"):
            st.subheader('Average Hourly data')
            st.write(da.head())
            
            
            
        if st.checkbox("click to subindex calculation"):
            st.markdown(""""**Lets do sub index calculation**
                            
    Sub index calculation can be done using concentration table as given in the picture.""")
            from PIL import Image
            image = Image.open('static/chart.png')
    
            st.image(image, caption="subindex Concetration table",width=600)
                
            from PIL import Image
            image = Image.open('static/formu.png')
    
            st.image(image, caption="Formula to be applied in concetration table",width=600)
                
            st.markdown("""** Procedure applied to obtain AQI **
                            
    1.Formula to be applied for PM10 by taking 24 hour average data. 
    
    2.Formula to be applied for SO2 by taking 24 hour average data.
    
    3.Formula to be applied for NOx by taking 24 hour average data.
    
    4.Formula to be applied for NO2 by taking 1 hour average data.
    
    5.Formula to be applied for CO by taking 8 hour average data.
    
    6.Formula to be applied for O3 by taking 8 hour average data.
    
    we have to do AQI bucketting (by comparing above concentration table)
                       
                """)
                
               
            
            st.subheader('Combined Pollutant AQI')
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = dsub.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="combined_AQI.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            st.write(dsub.head())
        st.text('© ASIA Consulting 2022')    
    elif choice == "Station wise Data":
        from PIL import Image
        image = Image.open('static/station.png')

        st.image(image, caption="Air Quality monitoring Station",width=600)
        st.subheader("Lets extract station wise Data")
        #lets check the station-1 hourly data
        if st.checkbox("Show station wise Data"):
            st.markdown("**Station 1**")
            st.write(station1.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station1.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="station1.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Station 2**")
            
            st.write(station2.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station2.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="station2.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Station 3**")
            
            st.write(station3.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station3.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="station3.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
                        
            st.markdown("**Station 4**")
            
            st.write(station4.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station4.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="station4.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)

            st.markdown("**Station 5**")
            
            st.write(station5.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station5.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base65,{b64}" download="station5.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Station 6**")
            
            st.write(station6.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station6.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base66,{b64}" download="station6.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.markdown("**Station 7**")
            
            st.write(station7.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station7.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base66,{b64}" download="station7.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
                        
            st.markdown("**Station 8**")
            
            st.write(station8.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station8.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base66,{b64}" download="station8.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)

            st.markdown("**Station 9**")
            
            st.write(station9.head())
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = station9.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base66,{b64}" download="station9.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
            
            st.subheader(""" We got all the station data """)
            
        if st.checkbox(""" Show average AQI Data for Each day"""):
            st.subheader("""Lets extract the Average Data of Each day from the year 2015 to year 2020""")
                
            st.write(Average_day.head())    
            
            import base64
            import io
            towrite = io.BytesIO()
            downloaded_file = Average_day.to_csv(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO buffer
            towrite.seek(0)  # reset pointer
            b64 = base64.b64encode(towrite.read()).decode() 
            linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base66,{b64}" download="Average_day_AQI.csv">Download csv file</a>'
            st.markdown(linko, unsafe_allow_html=True)
       
        st.text('© ASIA Consulting 2022')   
        
    elif choice == "Data Anlaysis":
        
        st.subheader("Data Analysis")
        from PIL import Image
        #image = Image.open('static/data.jpeg')

        st.image("https://www.esri.com/content/dam/esrisites/en-us/arcgis/capabilities/spatial-analysis/images/bigdata-realtime.gif", caption="Data Analysis",width=680)             
        
        if st.checkbox("Show the plots overall"):
            
            
            st.markdown("""**1️) Year vs Pollutant plots**""")
            ad=Average_day.copy()
            
            ad['Date'] = pd.to_datetime(ad['Date'])
            pollutants = ['PM10','NO2', 'CO', 'SO2','O3', 'NO','NOx']
            ad.set_index('Date',inplace=True)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(axes = ad[pollutants].plot(marker='.', alpha=0.5, linestyle='None', figsize=(20, 16), subplots=True))
            
            st.markdown("""**2) Station wise Plot**""")
            import matplotlib.pyplot as plt
            
            cols=['Combined_AQI']

            cmap=plt.get_cmap('Spectral')
            color=[cmap(i) for i in np.linspace(0,1,8)]
            explode=[0.2,0,0,0,0,0,0,0]
            fig, ax = plt.subplots()
            for col in cols:
                fig=plt.figure(figsize=(10,7))
    
            st.markdown('''**Grouping columns by station and 
            taking station average which have the highest affected**''')
    
            x=ad.groupby('Station')[col].mean().sort_values(ascending=False)
            x.reset_index('Station')
            #fig, ax = plt.subplots()
            x=x[:8].plot.pie(shadow=True,autopct='%1.1f%%',
                       colors=color,explode=explode,
                       wedgeprops={'edgecolor':'black','linewidth':0.4}
                       )
            
            st.pyplot(fig)
        
            st.markdown("""**🧐 Observation:**
                        
            From above pie chart we can conclude that Station 3 has highest AQI calculated.            
            """)
            
            st.markdown("""**3) Line plot analysis for amount of particulate matter over the years**""")
            
            ad.reset_index(inplace=True)
            ad['Month']=ad.Date.dt.month.astype(str)
            ad['Year']=ad.Date.dt.year.astype(str)
            import seaborn as sns
            cols=['PM10','NO2', 'CO', 'SO2','O3', 'NO','NOx']

            x=ad.iloc[:,2:]
            #fig=plt.figure(figsize=(15,24))
            fig, ax = plt.subplots()
            fig=plt.figure(figsize=(12,24))
            for i,col  in enumerate(cols):
                fig.add_subplot(4,2,i+1)
                sns.lineplot(x='Year',y=col,data=x)
            st.pyplot(fig)
            
            st.markdown(""" **🧐Observation:**
                        
               🔍 As we can observe above that how the pollutants has been increased or decreased over the years.
            
        1.we can say that CO and NO2 is the pollutant keep on changing over the years drastically.
            
        2.We can obseve NO is the most decreased pollutants over the years.
            
        3.PM10 is decreased after the year 2019""")
            
            
            
            cols=['Combined_AQI']
            
            st.markdown("""**4) AQI plot over the year**""")
            x=ad.iloc[:,2:]
            fig, ax = plt.subplots()
            fig=plt.figure(figsize=(12,24))
            for i,col  in enumerate(cols):
                fig.add_subplot(6,2,i+1)
                sns.lineplot(x='Year',y=col,data=x)
            st.pyplot(fig)
            
            st.markdown("""**🧐Observation:**
                        
        🔍 As the PM10 has been decereased My AQI calculted is also been decreased after 2019,
    so we can conclude that during the covid lockdown how my pollution is decreased. ✌️✌️✌️""")
    
        if st.checkbox("Show Station wise plots"):
            
            st.markdown("""**will check every station pollutant stats and there AQI with line plot with the average hour data**""")
            
            if st.checkbox("Show Station 1 Analysis"):
                
                st.subheader("**Station 1**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station1=s1.copy()
                station1.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station1['Date and Time'], y=station1['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)
                
                
            
            if st.checkbox("Show Station 2 Analysis"):
                station2=s2.copy()
                st.subheader("**Station 2**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station2.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station2['Date and Time'], y=station2['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)
    
            if st.checkbox("Show Station 3 Analysis"):
                station3=s3.copy()
                st.subheader("**Station 3**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station3.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station3['Date and Time'], y=station3['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)
                
            if st.checkbox("Show Station 4 Analysis"):
                station4=s4.copy()
                st.subheader("**Station 4**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station4.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station4['Date and Time'], y=station4['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)    
    
            if st.checkbox("Show Station 5 Analysis"):
                station5=s5.copy()
                st.subheader("**Station 5**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station5.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station5['Date and Time'], y=station5['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)
                
            if st.checkbox("Show Station 6 Analysis"):
                station6=s6.copy()
                st.subheader("**Station 6**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station6.reset_index(inplace=True) 
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station6['Date and Time'], y=station6['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)
                                      
            if st.checkbox("Show Station 7 Analysis"):
                station7=s7.copy()
                st.subheader("**Station 7**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station7.reset_index(inplace=True) 
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station7['Date and Time'], y=station7['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)       
        
            if st.checkbox("Show Station 8 Analysis"):
                station8=s8.copy()
                st.subheader("**Station 8**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station8.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station8['Date and Time'], y=station8['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig)   
        
            if st.checkbox("Show Station 9 Analysis"):
                station9=s9.copy()
                st.subheader("**Station 9**")
                st.markdown("""**On the figure below, we can see SO2, CO, PM10,NO,NOx,NO2 and O3 daily mean values. If we are interested only in some specific value, we can exclude rest from the image by clicking on variable names on the right side. For getting the closer look, we can zoom the image.**""")
                station9.reset_index(inplace=True)
                import plotly
                import plotly.graph_objects as go
                import plotly.express as px
                fig = go.Figure()
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['Combined_AQI'], mode='lines', name ='Combined_AQI',marker_color='#ff0000'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['PM10_24hr_avg'], mode='lines', name ='PM10_24hr_avg',marker_color='#0030A0'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['CO_8hr_max'], mode='lines', name ='CO_8hr_max',marker_color='BLACK'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['NOx_24hr_avg'], mode='lines', name ='NOx_24hr_avg',marker_color='firebrick'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['SO2_24hr_avg'], mode='lines', name ='SO2_24hr_avg',marker_color='darkorchid'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['O3_8hr_max'], mode='lines', name ='O3_8hr_max',marker_color='limegreen'))
                fig.add_traces(go.Scatter(x=station9['Date and Time'], y=station9['NO2_1hr_avg'], mode='lines', name ='NO2_1hr_avg',marker_color='#6ac3ec'))
                st.write(fig) 
    
        st.text('© ASIA Consulting 2022')
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
if __name__=='__main__':
    main()
        


