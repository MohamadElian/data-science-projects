import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


# Load and clean the dataset
df = pd.read_csv("Forecasting data-Mohamad.csv")
df.columns = df.columns.str.strip()
df['Month/Year'] = pd.to_datetime(df['Month/Year'], format="%B %Y")
df.set_index('Month/Year', inplace=True)

# Prepare data 
df_reset = df.reset_index()
df_reset['Month_Num'] = np.arange(len(df_reset))



# APRIL–AUGUST 2025: Linear Regression Forecast
future_apr_aug = pd.DataFrame({'Month_Num': np.arange(len(df_reset), len(df_reset) + 5)})
forecast_apr_aug = pd.DataFrame(index=pd.date_range(start="2025-04-01", periods=5, freq='MS'))

for column in df.columns:
    model = LinearRegression()
    if column != 'APP':
        model.fit(df_reset[['Month_Num']], df_reset[column])
        forecast_apr_aug[column] = model.predict(future_apr_aug)
        forecast_apr_aug[column] = forecast_apr_aug[column].round(0).astype(int)

for row in df.index:
    print(row)
    forecast_apr_aug['APP'] = forecast_apr_aug['Accessories']/forecast_apr_aug['Upgrades']


forecast_apr_aug = forecast_apr_aug.clip(lower=0)



# AUGUST–DECEMBER 2025: Bumped Linear Forecast
future_aug_dec = pd.DataFrame({'Month_Num': np.arange(len(df_reset) + 4, len(df_reset) + 9)})
forecast_aug_dec = pd.DataFrame(index=pd.date_range(start="2025-08-01", periods=5, freq='MS'))

for column in df.columns:
    model = LinearRegression()
    if column != 'APP':
        model.fit(df_reset[['Month_Num']], df_reset[column])
        predictions = model.predict(future_aug_dec)
        forecast_aug_dec[column] = predictions * 1.15  # 15% bump
        forecast_aug_dec[column] = forecast_aug_dec[column].round(0).astype(int)
    if column == 'APP':
        forecast_aug_dec['APP'] = forecast_aug_dec['Accessories']/forecast_aug_dec['Upgrades']    

forecast_aug_dec = forecast_aug_dec.clip(lower=0)

##for columns in df.columns:
##    if column != 'APP':
##        forecast_aug_dec[column] = forecast_aug_dec[column].round(0).astype(int)

# if column == 'APP':
#     forecast_aug_dec['APP'] = forecast_aug_dec['Accessories']/forecast_aug_dec['Upgrades']

# Combine April–July + Aug–Dec to get full 2025 forecast 
forecast_apr_jul = forecast_apr_aug.loc['2025-04-01':'2025-07-01']
forecast_2025_combined = pd.concat([forecast_apr_jul, forecast_aug_dec])

#  Combine original + 2025 forecast for seasonal 2026 modeling
full_data = pd.concat([df, forecast_2025_combined])
full_data = full_data.reset_index()
full_data.rename(columns={'index': 'Month/Year'}, inplace=True)
full_data['Year'] = full_data['Month/Year'].dt.year
full_data['Month'] = full_data['Month/Year'].dt.month

# 2026 Forecast: Seasonal regression (month-by-month)
forecast_2026 = []

for month in range(1, 13):
    month_data = full_data[full_data['Month'] == month].copy()
    month_data['Month_Index'] = np.arange(len(month_data))

    row = {}
    for column in df.columns:
        model = LinearRegression()
        if column != 'APP':
            model.fit(month_data[['Month_Index']], month_data[column])
            next_index = pd.DataFrame({'Month_Index': [len(month_data)]})
            prediction = model.predict(next_index)[0]
            row[column] = prediction
            

    forecast_2026.append(row)

# Finalize 2026 forecast 
forecast_2026_df = pd.DataFrame(forecast_2026, index=pd.date_range(start="2026-01-01", periods=12, freq='MS'))
forecast_2026_df = forecast_2026_df.clip(lower=0)

for column in df.columns:
    if column != 'APP':
        forecast_2026_df[column] = forecast_2026_df[column].round(0).astype(int)
if column == 'APP':
    forecast_2026_df['APP'] = forecast_2026_df['Accessories']/forecast_2026_df['Upgrades']

# printed all the data
print("-----------------------------------------------------------------")
print(" Origianal data")
print(df.round(2))
print("-----------------------------------------------------------------")

print(" Final Forecast: April–August 2025")
print(forecast_apr_aug.round(2))
print("-----------------------------------------------------------------")

print(" Final Forecast: Bumped August–December 2025")
print(forecast_aug_dec.round(2))
print("-----------------------------------------------------------------")

print(" Final Forecast: 2025 Combined")
print(forecast_2025_combined.round(2))
print("-----------------------------------------------------------------")

print(" Final Forecast: 2026 Seasonal")
print(forecast_2026_df.round(2))
print("-----------------------------------------------------------------")