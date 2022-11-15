import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import PredefinedSplit
import pandas_datareader as web
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout, LSTM

company = 'FB'
start = dt.datetime(2014,1,1)
end = dt.datetime(2022,1,1)

# define ticker symbol
data = web.DataReader(company, 'yahoo', start, end)

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

# how many days we want to look at the past to predict
prediction_days = 60

# defining two empty lists for preparing the training data
x_train = []
y_train = []

# we are counting from the 60th index to the last index
for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x-prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()
# specify the layer
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
# this is going to be a prediction of the next closing value
model.add(Dense(units=1))

# Load Test Data
test_start = dt.datetime(2022,10,1)
test_end = dt.datetime.now()

test_data = web.DataReader(company, 'yahoo', test_start, test_end)
actual_prices = test_data['Close'].values
total_dataset = pd.concat((data['Close'],test_data['Close']), axis=0)

model_input = total_dataset[len(total_dataset)- len(test_data) - prediction_days:].values
# reshaping the model
model_input = model_input.reshape(-1, 1)
# scaling down the model
model_input = scaler.transform(model_input)

x_test = []
for x in range(prediction_days, len(model_input)):
    x_test.append(model_input[x - prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_price = model.predict(x_test)
predicted_price = scaler.inverse_transform(predicted_price)

# plot the test Predictions
plt.plot(actual_prices, color="black", label=f"Actual{company} price")
plt.plot(predicted_price, color='green', label="Predicted {company} Price")
plt.title(f"{company} Share price")
plt.xlabel('Time')
plt.ylabel(f'{company} share price')
plt.legend
plt.show()

#prediction = model.predict(real_data)
#prediction = scaler.inverse_transform(prediction)
#print(f"Prediction: {prediction}")