
# coding: utf-8

# In[56]:

import tensorflow.contrib.keras as k
import numpy as np
import json

#RnnPredictor is the object that will recive the data, normalize it and predict if whe have to sell or buy

class RnnPredictor:
    def __init__(self):
        self.data = []
        self.normalised = np.array([])
        self.model = k.models.load_model("models/categorical_model_v006.h5")

    # in order to predict the model needs 30 prices with 1 minute of distance
    def recive(self,json_string):

        transaction_type, input_data = self.json_parse(json_string)
        
        if transaction_type == "match":            
            if len(self.data) == 30:
                data = self.data
                data = data[1:]
                data.append(input_data)
                self.data = data
                self.normalised = self.normalize_data()
            else:
                self.data.append(input_data)

    def publish(self):
        #until normalised is not a tensor of 3D we cannot compute the prediction
        if len(self.normalised.shape) == 3:
            prediction = self.model.predict(self.normalised)
            result = "BUY" if np.argmax(prediction) == 1 else "SELL"
        else:
            result = "MORE DATA"
        return result


    def normalize_data(self):
        data = self.data
        p0 = data[0]        
        normalised = np.array([(pi/p0)-1 for pi in data])
        normalised = normalised[np.newaxis,:,np.newaxis] 
        return normalised
    
    def json_parse(self,json_string):
        json_data = np.array([ p.split(":") for p in json_string.replace("{","").replace("}","").replace("'","").replace(" ","").split(",")])
        
        transaction_type = json_data[0][1]
        input_data = float(json_data[6][1])
        
        return transaction_type, input_data

