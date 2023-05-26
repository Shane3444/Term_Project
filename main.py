import pandas as pd
import streamlit as st
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.serialize import model_from_json
from sklearn.metrics import mean_squared_error

st.title("Stock Price Prediction")
model_name = st.sidebar.selectbox("Select Model for prediction", ("ARIMA", "Facebook Prophet", "Stacked LSTM", "All Models"))
data_set = st.selectbox("Select Stock for prediction", ("RELIANCE", "TATA", "SBI", "ICICI", "ADANI"))

def get_dataset():
        if data_set=="RELIANCE":
            data = yf.download('RELIANCE.NS', end='2023-05-01', auto_adjust=True)
            st.subheader('RELIANCE Raw Data')
            st.write(data.tail())
            st.subheader("Closing Price vs Time chart for entire RELIANCE dataset")
            st.line_chart(data.Close, use_container_width=True)
        elif data_set=="TATA":
            data = yf.download('TATASTLLP.NS', end='2023-05-01', auto_adjust=True)
            st.subheader('TATA STEEL Raw Data')
            st.write(data.tail())
            st.subheader("Closing Price vs Time chart for entire TATA STEEL dataset")
            st.line_chart(data.Close, use_container_width=True)
        elif data_set=="SBI":
            data = yf.download('SBIN.NS', end='2023-05-01', auto_adjust=True)
            st.subheader('SBI Raw Data')
            st.write(data.tail())
            st.subheader("Closing Price vs Time chart for entire SBI dataset")
            st.line_chart(data.Close, use_container_width=True)
        elif data_set=="ICICI":
            data = yf.download('ICICIBANK.NS', end='2023-05-01', auto_adjust=True)
            st.subheader('ICICI Raw Data')
            st.write(data.tail())
            st.subheader("Closing Price vs Time chart for entire ICICI dataset")
            st.line_chart(data.Close, use_container_width=True)
        elif data_set=="ADANI":
            data = yf.download('ADANIENT.NS', end='2023-05-01', auto_adjust=True)
            st.subheader('ADANI Raw Data')
            st.write(data.tail())
            st.subheader("Closing Price vs Time chart for entire ADANI dataset")
            st.line_chart(data.Close, use_container_width=True)
        # Split data into training and testing sets
        size = int(len(data.Close) * 0.9)
        train_data = list(data[0:size]['Close'])
        test_data = list(data[size:]['Close'])
        return data, train_data, test_data

data, train_data, test_data = get_dataset()

if model_name=="ARIMA":
    st.subheader(model_name)
    if data_set == "RELIANCE":
        predictions = pd.read_csv("./arima_predictions_reliance.csv")
    elif data_set == "TATA":
        predictions = pd.read_csv("./arima_predictions_tata.csv")
    elif data_set == "SBI":
        predictions = pd.read_csv("./arima_predictions_sbi.csv")
    elif data_set == "ICICI":
        predictions = pd.read_csv("./arima_predictions_icici.csv")
    elif data_set == "ADANI":
        predictions = pd.read_csv("./arima_predictions_adani.csv")

    # plt.title("Reliance NSE Closing Stock Price Since 1996")
    st.subheader("ARIMA predictions mapping Actual Dataset")
    fig2 = plt.figure(figsize=(20, 8), dpi=300)
    date_range = data[int(len(data.Close) * 0.9):].index
    plt.plot(date_range, predictions["actual_data"], color='blue', marker='.', label='Actual')
    plt.plot(date_range, predictions["predictions"], color='red', marker='.', linestyle='--', label='Predictions')
    plt.xlabel("Date")
    plt.ylabel("Closing Prices (Rs)")
    plt.grid()
    plt.legend()
    st.pyplot(fig2)
    rmse_1 = np.sqrt(np.square(np.subtract(predictions["actual_data"], predictions["predictions"])).mean()).round(2)
    st.write("RMSE: ", rmse_1)

    days = st.slider(label="Select days", value=14)
    st.subheader(f"ARIMA predictions for last {days} days")
    fig3 = plt.figure(figsize=(20,8), dpi=300)
    date_range = data[int(len(data.Close) * 0.9):].index
    plt.plot(date_range[-days:], predictions["actual_data"][-days:], color='blue', marker='.', label='Actual')
    plt.plot(date_range[-days:], predictions["predictions"][-days:], color='red', marker='.', linestyle='--', label='Predictions')
    # plt.title("Reliance NSE stock closing price forecast for last 15 days")
    plt.xlabel("Date")
    plt.ylabel("Closing Prices (Rs)")
    plt.grid()
    plt.legend()
    st.pyplot(fig3)
    rmse = np.sqrt(np.square(np.subtract(predictions["actual_data"][-days:], predictions["predictions"][-days:])).mean()).round(2)
    st.write("RMSE: ", rmse)

    predictions['Date'] = pd.to_datetime(predictions['Date'])
    # Set the 'Date' column as the index
    predictions = predictions.set_index('Date')
    st.line_chart(predictions[["actual_data", "predictions"]], use_container_width=True)

elif model_name=="Facebook Prophet":
    st.subheader(model_name)
    if data_set == "RELIANCE":
        forecast = pd.read_csv("./prophet_reliance_forcast.csv")
        df = pd.read_csv("./prophet_reliance_df.csv")
        with open('reliance_model.json', 'r') as fin:
            m = model_from_json(fin.read())  # Load model
    elif data_set == "TATA":
        forecast = pd.read_csv("./prophet_tata_forcast.csv")
        df = pd.read_csv("./prophet_tata_df.csv")
        with open('tata_model.json', 'r') as fin:
            m = model_from_json(fin.read())  # Load model
    elif data_set == "SBI":
        forecast = pd.read_csv("./prophet_sbi_forcast.csv")
        df = pd.read_csv("./prophet_sbi_df.csv")
        with open('sbi_model.json', 'r') as fin:
            m = model_from_json(fin.read())  # Load model
    elif data_set == "ICICI":
        forecast = pd.read_csv("./prophet_icici_forcast.csv")
        df = pd.read_csv("./prophet_icici_df.csv")
        with open('icici_model.json', 'r') as fin:
            m = model_from_json(fin.read())  # Load model
    elif data_set == "ADANI":
        forecast = pd.read_csv("./prophet_adani_forcast.csv")
        df = pd.read_csv("./prophet_adani_df.csv")
        with open('adani_model.json', 'r') as fin:
            m = model_from_json(fin.read())  # Load model

    st.subheader(data_set)
    forecast = forecast.drop("Unnamed: 0", axis=1)
    st.write(forecast.head())
    forecast['ds'] = pd.to_datetime(forecast['ds'])
    st.subheader("Prophet model mapping entire dataset")
    fig1 = m.plot(forecast)
    st.write(fig1)
    st.write("RMSE for entire dataset: ", np.sqrt(mean_squared_error(forecast.yhat[:-15], df.y)))
    st.subheader("Prophet model Components")
    fig2 = plot_components_plotly(m, forecast)
    st.write(fig2)

elif model_name=="Stacked LSTM":
    st.subheader(model_name)
    if data_set == "RELIANCE":
        predictions = pd.read_csv("./lstm_preds.csv")
    elif data_set == "TATA":
        predictions = pd.read_csv("./lstm_preds_4.csv")
    elif data_set == "SBI":
        predictions = pd.read_csv("./lstm_preds_3.csv")
    elif data_set == "ICICI":
        predictions = pd.read_csv("./lstm_preds_2.csv")
    elif data_set == "ADANI":
        predictions = pd.read_csv("./lstm_preds_5.csv")
    predictions['Date'] = pd.to_datetime(predictions['Date'])
    # Set the 'Date' column as the index
    predictions = predictions.set_index('Date')
    st.subheader("Stacked LSTM Predictions Mapping Testing Set")
    fig2 = plt.figure(figsize=(20, 8), dpi=300)
    date_range = data[int(len(data.Close) * 0.9):].index
    plt.plot(predictions["close"], color='blue', marker='.', label='Actual')
    plt.plot(predictions["yhat"], color='red', marker='.', linestyle='--', label='Predictions')
    plt.title("Reliance NSE Closing Stock Price Since 1996")
    plt.xlabel("Date")
    plt.ylabel("Closing Prices (Rs)")
    plt.grid()
    plt.legend()
    st.pyplot(fig2)

    st.subheader("Interactive Plot")
    st.line_chart(predictions, use_container_width=True)
    # st.line_chart(data=predictions, y=["actual_data", "predictions"])

    days = st.slider(label="Select days", value=14)
    st.subheader(f"Stacked LSTM predictions for last {days} days")
    fig3 = plt.figure(figsize=(20, 8), dpi=300)
    date_range = data[int(len(data.Close) * 0.9):].index
    plt.plot(date_range[-days:], predictions["close"][-days:], color='blue', marker='.', label='Actual')
    plt.plot(date_range[-days:], predictions["yhat"][-days:], color='red', marker='.', linestyle='--',
             label='Predictions')
    # plt.title("Reliance NSE stock closing price forecast for last 15 days")
    plt.xlabel("Date")
    plt.ylabel("Closing Prices (Rs)")
    plt.grid()
    plt.legend()
    st.pyplot(fig3)
    rmse = np.sqrt(np.square(np.subtract(predictions["close"][-days:], predictions["yhat"][-days:])).mean()).round(2)
    st.write("RMSE: ", rmse)
else:
    if data_set == "RELIANCE":
        predictions_arima = pd.read_csv("./arima_predictions_reliance.csv")
        predictions_lstm = pd.read_csv("./lstm_preds.csv")
    elif data_set == "TATA":
        predictions_arima = pd.read_csv("./arima_predictions_tata.csv")
        predictions_lstm = pd.read_csv("./lstm_preds_4.csv")
    elif data_set == "SBI":
        predictions_arima = pd.read_csv("./arima_predictions_sbi.csv")
        predictions_lstm = pd.read_csv("./lstm_preds_3.csv")
    elif data_set == "ICICI":
        predictions_arima = pd.read_csv("./arima_predictions_icici.csv")
        predictions_lstm = pd.read_csv("./lstm_preds_2.csv")
    elif data_set == "ADANI":
        predictions_arima = pd.read_csv("./arima_predictions_adani.csv")
        predictions_lstm = pd.read_csv("./lstm_preds_5.csv")

    days = st.slider(label="Select days", value=14)
    st.subheader(f"Predictions for last {days} days")
    fig3 = plt.figure(figsize=(20, 8), dpi=300)
    date_range = data[int(len(data.Close) * 0.9):].index
    plt.plot(date_range[-days:], predictions_arima["actual_data"][-days:], color='blue', marker='.', label='Actual Data')
    plt.plot(date_range[-days:], predictions_arima["predictions"][-days:], color='red', marker='.', linestyle='--',
             label='ARIMA Predictions')
    plt.plot(date_range[-days:], predictions_lstm["yhat"][-days:], color='green', marker='.', linestyle='--',
             label='LSTM Predictions')
    # plt.title("Reliance NSE stock closing price forecast for last 15 days")
    plt.xlabel("Date")
    plt.ylabel("Closing Prices (Rs)")
    plt.grid()
    plt.legend()
    st.pyplot(fig3)
    rmse_arima = np.sqrt(
        np.square(np.subtract(predictions_arima["actual_data"][-days:], predictions_arima["predictions"][-days:])).mean()).round(2)
    rmse_lstm = np.sqrt(np.square(np.subtract(predictions_lstm["close"][-days:], predictions_lstm["yhat"][-days:])).mean()).round(2)

    st.write("RMSE ARIMA: ", rmse_arima)
    st.write("RMSE LSTM:", rmse_lstm)
