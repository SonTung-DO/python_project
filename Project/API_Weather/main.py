import sys
import requests
from PyQt5.QtWidgets import ( QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout )
from PyQt5.QtCore import Qt

class WeatherApp ( QWidget ): # QWidget is used to display GUI, content on a custom rectangle on our screen
    def __init__(self):
        super().__init__()
        self.city_label = QLabel(" Enter the city label you want ", self )
        self.city = QLineEdit(self)
        self.get_temp_button = QPushButton(" Get temperature ", self)
        self.temp_label = QLabel(self)
        self.emote_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("SUPER COOL WEATHER APP") # This change the name/title of the app
        
        #All this code below help arrange UI in the left of the window 
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city)
        vbox.addWidget(self.get_temp_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emote_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # This will align all of those message to the middle of the app's window, like in CSS
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emote_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Set this class variable to a specified name to CSS usage
        self.city_label.setObjectName("city_label")
        self.city.setObjectName("city")
        self.get_temp_button.setObjectName("get_temp_button")
        self.temp_label.setObjectName("temp_label")
        self.emote_label.setObjectName("emote_label")
        self.description_label.setObjectName("description_label")
                
        # CSS
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family : calibri;
            }                
            QLabel#city_label {
                font-size : 40px;
            }
            QLineEdit#city {
                font-size : 40px;
            }
            QPushButton#get_temp_button {
                font-size : 30px;
                font-weight : bold;
            }
            QLabel#temp_label {
                font-size : 70px;
            }
            QLabel#emote_label {
                font-size : 110px;
                font-family : Segoe UI emoji;
            }
            QLabel#description_label {
                
            }
        """)
        
        self.get_temp_button.clicked.connect(self.get_weather_city)

        
    def get_weather_city(self) :
        
        api_key = "78079516b50dc59815d226a4ad2fe24b"
        city = self.city.text()
        link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            res = requests.get(link)
            res.raise_for_status() # This will raise an exception if there are any HTTP error
            data = res.json()        
            if data["cod"] == 200 : # Verify that the request is success
                self.weather_display(data)
        except requests.exceptions.HTTPError as http_error: # Name this as http_error ( kinda like SQL lol )
            match res.status_code:
                case 400 :
                    self.error_display("Bad request :\n Please re-check your input")
                case 401 :
                    self.error_display("Unauthorized :\n Invalid API key")
                case 403 :
                    self.error_display("Forbidden :\n Access denied")
                case 404 :
                    self.error_display("Request not found! The city may not exist :\n Please try again")
                case 500 :
                    self.error_display("Internal server error :\n Please try again later")
                case 502 :
                    self.error_display("Bad gateaway :\n Invalid response from the upstream server")
                case 503 :
                    self.error_display("Service unavailable :\n The server cannot handle the request")
                case 504 :
                    self.error_display("Gateaway timeout :\n Didn't receive a timely response from the upstream server")
                case _:
                    self.error_display(f"HTTP error occured :\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.error_display("Connection error :\n Please check your internet connection")
        except requests.exceptions.Timeout:
            self.error_display("Timeout error :\n Resquest timed out")
        except requests.exceptions.TooManyRedirects:
            self.error_display("Too many redirect :\n Please check the URL")
        except requests.exceptions.RequestException as request_error :
            self.error_display(f"Request error :\n {request_error}")

    
    def error_display(self, msg) :
        self.temp_label.setStyleSheet("font-size : 25px;")
        self.temp_label.setText(msg) # THis will display the error message in our app's window
        self.emote_label.clear()
        self.description_label.clear()
    
    def weather_display(self,data) :
        self.temp_label.setStyleSheet("font-size : 70px;")
        self.description_label.setStyleSheet("font-size : 70px")
        temperature_in_kelvin = data["main"]["temp"]
        temperature_in_celsious = temperature_in_kelvin - 273.15
        weather_des = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        
        self.temp_label.setText(f"{temperature_in_celsious:.0f}°C")
        self.emote_label.setText(self.get_emoji_weather(weather_id))
        self.description_label.setText(weather_des)
        
    @staticmethod
    def get_emoji_weather(id):
        if 200 <= id <= 232:
            return "⛈️"
        elif 300 <= id <= 321:
            return "🌦"
        elif 500 <= id <= 531:
            return "🌧️"
        elif 600 <= id <= 622:
            return "❄️"
        elif 701 <= id <= 741:
            return "💨"
        elif id == 781:
            return "🌪️"
        elif id == 800:
            return "☀️"
        elif 801 <= id <= 804:
            return "☁️"
        else:
            return " No symbol can represent this type of weather lol "
    
if __name__ == "__main__": # If this file is the file where we run directly, the name will be main
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show() # This method will run the GUI/content on our computer's screen, but only for a split second
    sys.exit(app.exec_()) # This method help the window (GUI) to stay open 