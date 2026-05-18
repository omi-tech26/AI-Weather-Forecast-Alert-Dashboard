from sklearn.linear_model import LinearRegression
import numpy as np
import random

def predict_temperature(current_temp):

    days = np.array([1,2,3,4,5]).reshape(-1,1)

    temps = np.array([
        current_temp - random.randint(1,3),
        current_temp,
        current_temp + random.randint(1,2),
        current_temp + random.randint(2,4),
        current_temp + random.randint(1,5)
    ])

    model = LinearRegression()

    model.fit(days,temps)

    prediction = model.predict([[6]])

    return round(prediction[0],2)