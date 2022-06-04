
from email import message
import requests
class Messenger():
    def __init__(self):
        print("Messenger initialised")
        self.bot_token = "5486965574:AAF4a-22us68EJdgfqXTT_mp87LlX3jo0cc"
        self.chatID = self.get_chatID()
        pass
    def get_chatID(self):
        print("Getting chatID")
        chatID = "chat_id"
        get_chatID = 'https://api.telegram.org/bot' + self.bot_token + '/getUpdates'
        response = requests.get(get_chatID)
        chatID = response.json()['result'][0]['message']['from']['id']
        return chatID
    def send_message(self, message):
        print("Sending message: " + message)
        # r = requests.post("http://localhost:5000/message", data={"message": message})
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + str(self.chatID) + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
        return response.json()

m = Messenger()
# print(response_1)
res = m.send_message("Hello World")
print(res)

import keras.callbacks
class CallBackNotifier(keras.callbacks.Callback):
    def __init__(self, checkpoints, messenger):
        self.completed = False
        self.messenger = messenger
    def on_train_end(self, logs = None):
        print("Message from CustomCallBackNotifier")
        keys = list(logs.keys())
        print("Stop training; got log keys: {}".format(keys))
        res_finished = self.messenger.send_message("Finished training model")

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
loss_tracker = keras.metrics.Mean(name="loss")
mae_metric = keras.metrics.MeanAbsoluteError(name="mae")
class CustomModel(keras.Model):
    def train_step(self, data):
        x, y = data

        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)  # Forward pass
            # Compute our own loss
            loss = keras.losses.mean_squared_error(y, y_pred)

        # Compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Compute our own metrics
        loss_tracker.update_state(loss)
        mae_metric.update_state(y, y_pred)
        return {"loss": loss_tracker.result(), "mae": mae_metric.result()}

    @property
    def metrics(self):
        # We list our `Metric` objects here so that `reset_states()` can be
        # called automatically at the start of each epoch
        # or at the start of `evaluate()`.
        # If you don't implement this property, you have to call
        # `reset_states()` yourself at the time of your choosing.
        return [loss_tracker, mae_metric]

    
ds = tfds.load('mnist', split='train', shuffle_files=True)
inputs = keras.Input(shape=(32,))
outputs = keras.layers.Dense(1)(inputs)
model = CustomModel(inputs, outputs)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

import numpy as np

# Just use `fit` as usual -- you can use callbacks, etc.
x = np.random.random((1000, 32))
y = np.random.random((1000, 1))
messenger = Messenger()
model.fit(x, y, epochs=5, callbacks = [CallBackNotifier(checkpoints= [1], messenger = messenger)])