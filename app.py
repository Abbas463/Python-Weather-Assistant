import pyttsx3
import datetime
import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty("rate", 150)  # Adjust speech speed
    engine.say(text)
    engine.runAndWait()

# Function to get the time of day
def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 20:
        return "evening"
    else:
        return "night"

# Function to get weather information
def get_weather(province, country):
    api_key = "6b62661cb2ca42a681674104252901"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={province},{country}&aqi=no"

    try:
        response = requests.get(url)
        data = response.json()
        if "current" in data:
            temp = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            return temp, condition
    except:
        pass
    return None, None

# Function to format temperature
def format_temperature(temp):
    return f"{temp:+.1f}°C" if temp is not None else "N/A"

# Function to fetch country list
def get_country_list():
    url = "https://countriesnow.space/api/v0.1/countries/states"
    try:
        response = requests.get(url)
        countries = [item["name"] for item in response.json()["data"]]
        return sorted(countries)
    except:
        return ['Afghanistan']

# Function to fetch provinces/states for a country
def get_province_list(country):
    url = "https://countriesnow.space/api/v0.1/countries/states"
    try:
        response = requests.post(url, json={"country": country})
        states = [state["name"] for state in response.json().get("data", {}).get("states", [])]
        return sorted(states) if states else []
    except:
        return []

# Function to update province dropdown when country changes
def update_provinces(event=None):
    country = country_combobox.get()
    if country:
        provinces = get_province_list(country)
        province_combobox["values"] = provinces if provinces else ["No provinces available"]
        province_combobox.current(0)

# Function to handle placeholder text correctly
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")  # Change text color to black when typing

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")  # Change text color back to gray if empty

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Function to handle submission
def on_submit():
    name = name_entry.get()
    country = country_combobox.get()
    province = province_combobox.get()

    if name in ["Enter your name", ""] or country == "Select Your Country" or province == "Select Your Province":
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    time_of_day = get_time_of_day()
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    temp, weather = get_weather(province, country)

    greeting = f"Hello {name}, good {time_of_day}. It is {current_time}."
    weather_report = f"The current temperature in {province}, {country} is {format_temperature(temp)} with {weather}." if temp is not None else "I couldn't retrieve the weather information."
    final_message = f"{greeting} {weather_report}"

    print(final_message)
    speak(final_message)

# Create main window
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("800x600")
root.config(bg="#343434")
root.resizable(False, False)

# Load and display logo (Centered)
logo_path = r"C:\Users\SHC\Desktop\Project\Voice Assistant\Logo.png"
logo_image = Image.open(logo_path).resize((200, 200))
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo, bg="#343434")
logo_label.pack(pady=20)

# Form Frame
form_frame = tk.Frame(root, bg="#343434")
form_frame.pack(pady=10)

# Name Input with Placeholder (Now text appears black when typing)
name_entry = tk.Entry(form_frame, width=30, font=("Arial", 14), fg="gray", bg="white", insertbackground="black")
name_entry.grid(row=0, column=0, padx=10, pady=5)
add_placeholder(name_entry, "Enter your name")

# Country Selection with Placeholder
country_combobox = ttk.Combobox(form_frame, values=get_country_list(), width=27, font=("Arial", 14))
country_combobox.grid(row=1, column=0, padx=10, pady=5)
country_combobox.set("Select Your Country")
country_combobox.bind("<<ComboboxSelected>>", update_provinces)

# Province Selection with Placeholder
province_combobox = ttk.Combobox(form_frame, values=["Select Your Province"], width=27, font=("Arial", 14))
province_combobox.grid(row=2, column=0, padx=10, pady=5)
province_combobox.set("Select Your Province")

# Submit Button
submit_button = tk.Button(root, text="Submit", bg="white", fg="black", font=("Arial", 14), command=on_submit)
submit_button.pack(pady=20)

# Run Application
root.mainloop()
