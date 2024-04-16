import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from tkinter import *
import customtkinter
import openpyxl
from datetime import datetime

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

flag =  True
flag2 =  True
programStarting = True
sliding = False


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "iot-greenhouse-fb219",
  "private_key_id": "77c85c8dfc015a9aa0c0790e892a81e9366f7545",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHl0CTNjLMT5k3\nbn0PRdzEQ9uvS9TAelMz/Y590GYQrrIfQdEV7BM3HQYskxU9BG+R+2PKbLHUcZqr\nIU0pnm3fkR5t5RTVNGH/Ds0aX7OZTGuB2hTZYKXNZSet56aU3Rgh3jxW6OgqoKQ7\n6u34SqBAZWlh8TfqOc03NbIC2drFPHkTN16htESrQKaW637GEVk6YBoonXlebIIt\nZhZ0dg6Ct1AvRYA5UsE9hG2+qenn0LuZT7WBUYQtjl5zYhcSrlf052bcoQ2i27p/\ny8JbZFVOqyBiGjlOZdiMXb6DIQeHknx/kRzO88M+LR+f+7jk6H03ozisiuNHpuUi\nyeeXNhZJAgMBAAECggEADSp67+MOv4e+KogLL51bCmbUCGibCo3fLHIsyrubKf1O\nIm316AlsPJHZcQoMR/vBjNqNiwI3ylTqoCCInabV5l4lKNhoUwabMsckDDn1J9cA\nzf5n6u17TnTeZNQ/urjpcT1+0zhWrU4uu0WcaEkq8EiIRrXR641fzkUoXpQGoIVG\nehgJ2RMfAYP1zY7uur4w3xxGkeg8++UAfpVAatm8kHhZo/BVk3BsYwMPLuazoJ+j\nFUYp+AbEqFRlFWg5AhcOeuVzAHeUD8K/Mb5Tl57Tf/u5TzHTh85NYDVH3GqAuQQE\nnKD/sgeHFTYdFehxsC0Twp9Jc0GQfMG+BKj6eeEEkQKBgQDraOukRsu5lBywTvXv\nfLsgSkKjtDB6h8UnheMEGxMP1TGkkjvcAceAzr6SCDp8ft/G5HXyQhE5YzGziL/9\nsw3bcDT3qasqyFa8Y7vyfjcnTREcWewaQUsP4doNNeJ8VkxbduYAh5Oo/ibe9vmx\nGE3i8YPpZhw2sXB3Gj3gVqzmGQKBgQDZDE40JExAaQ+d/QHDchyt8lHQbF5vRnSF\n/QNqdQgaSFsfzRfh1IyHGpt6M0j8oLcAGJft4u0VCdL3CUJyiPLf3xo7Y8AFC7mS\ncoQ59A28btuDlOC0ZuipRBU8LL/9cStET40imTbOp1Da5yOV7wmQLFDiY2zgOCI8\nTCC/7UzXsQKBgAUITClJ3icMdISMW5OQDgwFqmEHhBXKezt6ED1ROtoWy6Xh/meY\nniQxxz8l7+IjcDM3RRI1uVqJtVFKNhh9UGmFf4xf0ynp+Hi0hRsM+a7cZeY+Qd7Z\n0Hn5cQjhQwM3cRBvfUE7pLtzG2+exf20ME4Oraw6o5XDu0zAgdwe3jlZAoGAAqSR\ntzTR8N7Wn9fa06RqEPwoXt9S7wvuk0sXZY5zQM6svWBj8A4EgAik6AID23+hetDR\n2MWwmVb7SKLGOlrMiklPKnX2epk/8zaNwZ7lI+w9pAaGDexK3PTFRWxOEin0mupV\nD5zJ/A4xf9jcqBC3DxhbC8amJrzIPe+3Xl7nVqECgYEAi4CdXEFx/KTWQ1Ssnnz3\n9mbVw/RukxqggGFiAo/UN1ZKhSAImoEuRdKjB5D2TuesQ44bkDcqEjjtiixgoABT\nhyMutNcfE3t94ELgPiHEABqX6/IsOiW9bgtMAtfUi6SVUZevvM1lTlMGyMFjurwX\ngKiKp3N5x5nk7uE9MCYog4I=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-kgfje@iot-greenhouse-fb219.iam.gserviceaccount.com",
  "client_id": "107717164848226428469",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-kgfje%40iot-greenhouse-fb219.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)




config = {
  "apiKey": "AIzaSyCRYmX_VwVX7j3_b2V9nAayLuEaa7NzCbI",
  "authDomain": "iot-greenhouse-fb219.firebaseapp.com",
  "databaseURL": "https://iot-greenhouse-fb219-default-rtdb.firebaseio.com",
  "projectId": "iot-greenhouse-fb219",
  "storageBucket": "iot-greenhouse-fb219.appspot.com",
  "messagingSenderId": "119653996032",
  "appId": "1:119653996032:web:e55e99fde69116dfb4aae5",
 
};

#excel headers
workbook = openpyxl.Workbook()
sheet = workbook.active
headers = ["Timestamp", "Fan", "Humidity", "Motion","Pump status","Slider_val","Soil_Moisture","Temperature"]
sheet.append(headers)


firebase = pyrebase.initialize_app(config)

sensor_node = "Data"

db = firebase.database()
dbStore = firestore.client()








# Pass the user's idToken to the push method
#db.child("Data").set(data)

#define a function for mode button
def send_data(data):
    db.child("Data").update(data)

def Pump_Change():
    global flag
    if flag:
        flag = False
        send_data({"Pump status":0})
        
    else:
        flag = True
        send_data({"Pump status":1})

def FAN_Change():
    global flag2
    print(flag2)
    if flag2:
        flag2 = False
        send_data({"Fan":0})
        
    else:
        flag2 = True
        send_data({"Fan":1})
 

def updateValue(event):
        val = slider_1.get()
        send_data({"Slider_val":val})

def Update_GUI(data):
    if data.get("Temperature"):
        Temperature = data.get("Temperature")
        lbl2.config(text=f"{Temperature}°C")
        
    if data.get("Humidity"):
        Humidity = data.get("Humidity")
        lbl4.config(text=f"{Humidity} %")

    if data.get("Soil_Moisture") or data.get("Soil_Moisture") == 0:
        Soil_Moisture = data.get("Soil_Moisture")
        lbl6.config(text=f"{Soil_Moisture} %")


    global flag2
    if data.get("Fan")!=None:
        if data.get("Fan"):
            Fan_Status = "ON"
            btn2.configure(text = "Turn Off Fan", fg_color = "blue")
            
        else:
            Fan_Status = "OFF"
            btn2.configure(text = "Turn On Fan", fg_color = "green")
            flag2 = False
        lbl8.config(text=f"{Fan_Status}")
    
    global flag
    if data.get("Pump status") != None:
        if data.get("Pump status"):
            Pump_Status = "ON"
            btn1.configure(text = "Turn Off Pump", fg_color = "blue")
        else:
            Pump_Status = "OFF"
            btn1.configure(text = "Turn On Pump", fg_color = "green")
            flag = False
        lbl10.config(text=f"{Pump_Status}")

    if data.get("Slider_val") != None:
        Slider_val = int(data.get("Slider_val"))
        slider_1.set(Slider_val)
        lbl11.config(text=f"Light Level : {Slider_val}")

    if (data.get("Motion") != None) or (data.get("Motion") == 0):
        if data.get("Motion"):
            lbl13.config(text=f"Yes")
        else:
            lbl13.config(text=f"No")
    

def stream_handler(message):
    print(message["event"]) 
    print(message["path"]) 
    print(message["data"]) 
    
    Update_GUI(message["data"])
    all_data = db.child("Data").get()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([timestamp,all_data.val().get("Fan"),all_data.val().get("Humidity"),all_data.val().get("Motion"),all_data.val().get("Pump status"),all_data.val().get("Slider_val"),all_data.val().get("Soil_Moisture"),all_data.val().get("Temperature")])
    dbStore.collection('Data').document(timestamp).set({'Fan':all_data.val().get("Fan"),'Humidity':all_data.val().get("Humidity"),'Motion':all_data.val().get("Motion"),'Pump status':all_data.val().get("Pump status"),'Slider_val':all_data.val().get("Slider_val"),'Soil_Moisture':all_data.val().get("Soil_Moisture"),'Temperature':all_data.val().get("Temperature")})

window = customtkinter.CTk()

window.geometry('475x330')
window.title("Greenhouse App")

upperFrame = customtkinter.CTkFrame(window, corner_radius = 10, width = 5000)
upperFrame.grid(row = 0, column = 0, padx=10, pady=10, sticky="nsew")

my_labelframe = customtkinter.CTkFrame(upperFrame,width = 500, corner_radius = 10)
my_labelframe.grid(row = 0, column = 0, padx=10, pady=10, sticky="w")

my_sliderframe = customtkinter.CTkFrame(upperFrame, corner_radius = 10)
my_sliderframe.grid(row = 0, column = 1, padx=10, pady=5, sticky="e")

my_btnframe = customtkinter.CTkFrame(window, width=400, corner_radius = 10)
my_btnframe.grid(row = 1, column = 0, padx=10, pady=5, sticky="nsew")
                  
lbl1 = Label(my_labelframe, text="Temperature :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl1.grid(row = 0, column = 0, padx=10, pady=5, sticky="w")

lbl2 = Label(my_labelframe, text="25°C", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl2.grid(row = 0, column = 1, padx=10, pady=5, sticky="e")

lbl3 = Label(my_labelframe, text="Humidity :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl3.grid(row = 1, column = 0, padx=10, pady=5, sticky="w")

lbl4 = Label(my_labelframe, text="50%", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl4.grid(row = 1, column = 1, padx=10, pady=5, sticky="e")

lbl5 = Label(my_labelframe, text="Soil_Moisture :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl5.grid(row = 2, column = 0, padx=10, pady=5, sticky="w")

lbl6 = Label(my_labelframe, text="Medium", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl6.grid(row = 2, column = 1, padx=10, pady=5, sticky="e")

lbl7 = Label(my_labelframe, text="Fan Status :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl7.grid(row = 3, column = 0, padx=10, pady=5, sticky="w")

lbl8 = Label(my_labelframe, text="-", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl8.grid(row = 3, column = 1, padx=10, pady=5, sticky="e")

lbl9 = Label(my_labelframe, text="Pump Status :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl9.grid(row = 4, column = 0, padx=10, pady=5, sticky="w")

lbl10 = Label(my_labelframe, text="-", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl10.grid(row = 4, column = 1, padx=10, pady=5, sticky="e")

lbl12 = Label(my_labelframe, text="Motion detected :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl12.grid(row = 5, column = 0, padx=10, pady=5, sticky="w")

lbl13 = Label(my_labelframe, text="-", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl13.grid(row = 5, column = 1, padx=10, pady=5, sticky="e")

lbl11 = Label(my_sliderframe, text="Light Level :", bg="#323332", fg="#ffffff", font=("Helvetica", 12))
lbl11.grid(row = 0, column = 0, padx=10, pady=5, sticky="w")

btn1 = customtkinter.CTkButton(my_btnframe, text = "Pump", command = Pump_Change)
btn1.grid(row = 0, column = 1, padx = 40, pady = 20)

btn2 = customtkinter.CTkButton(my_btnframe, text = "FAN", command = FAN_Change)
btn2.grid(row = 0, column = 0, padx = 40, pady = 20)

slider_1 = customtkinter.CTkSlider(my_sliderframe,from_=0, to=100)
slider_1.grid(row = 1, column = 0, pady = 20)
slider_1.bind("<ButtonRelease-1>",updateValue)
slider_1.set(50)

my_stream = db.child("Data").stream(stream_handler)
window.mainloop()

workbook.save("Data.xlsx")
