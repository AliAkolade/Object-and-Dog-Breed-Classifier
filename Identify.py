from PIL import Image
import numpy as np
from keras.models import load_model
import tkinter
from tkinter import filedialog
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import tkinter
from tkinter import filedialog
import PIL
from PIL import Image
import requests


model = load_model('New_Trained_model.h5')
url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'


# noinspection PyBroadException
class MyBox(BoxLayout):

    def identify(self):
        labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        input_path = filedialog.askopenfilename()
        input_image = Image.open(input_path).resize((32, 32), resample=Image.LANCZOS)
        image_array = np.array(input_image).astype('float32')
        image_array /= 255.0
        image_array = image_array.reshape(1, 32, 32, 3)
        answer = model.predict(image_array)
        # noinspection PyTypeChecker
        self.ans.text = str(labels[np.argmax(answer)]).title()

        try:
            if self.ans.text == "Dog":
                path = input_path
                data = {'file': open(path, 'rb'), 'modelId': ('', '052e52ea-845f-4b4a-9fe1-b27dd2eb19d6')}
                response = requests.post(url, auth=requests.auth.HTTPBasicAuth('5Ner4sKSl0ikoPQ074_35YoNk9JBX__W', ''),
                                         files=data)
                a = response.text.replace("{\"message\":\"Success\",\"result\":[{\"message\":\"Success\","
                                          "\"prediction\":[{\"label\":\"", "").split("\"")
                label = a[0].replace("_", " ").title()
                self.ans.text = "Dog\nBreed - "+label
        except:
            self.ans.text = "Dog\nConnect to Internet to for breed"


class IdentifyApp(App):
    def build(self):
        return MyBox()


MyApp = IdentifyApp()
MyApp.run()
