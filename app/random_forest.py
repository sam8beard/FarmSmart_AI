from sklearn.model_selection import train_test_split
# splits a dataframe into training and testing subsets
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
# Model Choice: It seems that choosing a Regression Model would be a lot more effective for this because we are looking at the effect
# of time on a variable rather than classification

def random_forest():
    #read csv into a dataframe object
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'moisture_data.csv'))
    df = df.drop(['_id', 'sensor_id', 'report'], axis=1)

    #Predicting future moisture levels, need to do a time series predictor

    #So the issue here is that i only train the model based on the curretn moisture level and expect to get the current moisture level back
    #however, this won't work

    #instead I need to also include the past moisture levels in the current dataframe because the model will only train using the info in the current dataframe

    #so basically makes a copy of the moisture column puts it into a new column called moisture_lag_1 and shfits it down 1 row
    df['moisture_lag_1'] = df['moisture'].shift(1)
    df['moisture_lag_2'] = df['moisture'].shift(2)
    df['moisture_lag_3'] =df['moisture'].shift(3)
    #same for lag_2 so now I have two columns for comparing two past moisture values to a single current one

    #get rid of the first row after the data shift
    df = df.dropna()

    # This method constructs testing (80% of the data from dataframe) and training datasets 
    # X: array of the columns that will be used to train the model
    # y: array of the data column we are trying to predict

    X = df[['temperature', 'moisture_lag_1', 'moisture_lag_2', 'moisture_lag_3']]
    y = df['moisture']

    # print(f'X: {X.head()}')
    # print(f'y: {y.head()}')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # print(f'X_train_size: {X_train.shape}')
    # print(f'X_test_size: {X_test.shape}')
    # print(f'y_train_size: {y_train.shape}')
    # print(f'y_test_size: {y_test.shape}')

    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    #the max_depth parameter is useful for ensuring that the regression model doesn't overfit

    #TASK: MAKE SURE THAT I FINISH THE REGRESSION MODEL!!!

    regressor.fit(X_train, y_train)

    #prediction
    y_pred = regressor.predict(X_test)

    print(f'y_test: {y_test.size}')
    print(f'y_pred: {y_pred.size}')

    # print(f'MSE: {mean_squared_error(y_test, y_pred)}')

    timestamp = list(range(1,19))
    print(f'timestamp: {len(timestamp)}')

    d = {'timestamp': timestamp, 'y_test': y_test, 'y_pred': y_pred}

    df_table = pd.DataFrame(data=d)

    return df_table

    # plt.plot(y_test, y_pred)
    # plt.figure(figsize=(10, 6))
    # plt.plot(df_table['timestamp'], df_table['y_test'], label='Actual Moisture', marker='o')
    # plt.plot(df_table['timestamp'], df_table['y_pred'], label='Predicted Moisture', marker='x')

    # plt.title('Actual vs Predicted Moisture Levels')
    # plt.xlabel('Timestamp')
    # plt.ylabel('Moisture')
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    #basic scoring to quantify how well the actual data compares to the predicted


# if __name__ == "__main__":
#     random_forest()

    #So basically RandomForestRegressor is much better than DeepForestRegressor: the likelihood of underfitting is much lower
    # Reducing underfitting: training on a dataframe with more columns and data

    #Arrays or lists must be of the same size to be added to a dataframe