# Importar los módulos necesarios
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import io
from dotenv import load_dotenv
import os


load_dotenv()
API_key = os.getenv("WEATHER_API_KEY")

# Función para obtener información del clima desde OpenWeatherMap
def get_weather(city):
    if not API_key:
        messagebox.showerror("Error", "API Key no configurada.")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric&lang=es"
    try:
        res = requests.get(url)
        data = res.json()

        if res.status_code != 200 or data.get("cod") != 200:
            messagebox.showerror("Error", "Ciudad no encontrada.")
            return None

        return data

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        return None

# Buscar clima por ciudad
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    location = f"{result['name']}, {result['sys']['country']}"
    location_label.config(text=location)

    description = result['weather'][0]['description'].capitalize()
    temp = result['main']['temp']
    weather_label.config(text=f"{description}, {temp:.1f}°C")

    # Mostrar ícono del clima
    icon_code = result['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    image_data = requests.get(icon_url).content
    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
    image = image.resize((100, 100), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    icon_label.config(image=photo)
    icon_label.image = photo

# Ventana principal
root = ttkbootstrap.Window(themename="morph") 
root.title("Weather App")
root.geometry("400x600")
root.resizable(False, False)

# Contenedor principal
container = ttkbootstrap.Frame(root)
container.place(relx=0.5, rely=0.5, anchor="center")

# Cargar y mostrar el logo
logo_image = Image.open("assets/logo.png")
logo_image = logo_image.resize((190, 190), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = ttkbootstrap.Label(container, image=logo_photo)
logo_label.image = logo_photo  # mantener referencia
logo_label.pack(pady=(0, 5))

# Entrada de texto
city_entry = ttkbootstrap.Entry(container, font=("Segoe UI", 14), width=26, bootstyle="info")
# Placeholder manual
placeholder_text = "Ej: Santiago"
city_entry.insert(0, placeholder_text)

def clear_placeholder(event):
    if city_entry.get() == placeholder_text:
        city_entry.delete(0, tk.END)

def restore_placeholder(event):
    if city_entry.get() == "":
        city_entry.insert(0, placeholder_text)

city_entry.bind("<FocusIn>", clear_placeholder)
city_entry.bind("<FocusOut>", restore_placeholder)
city_entry.pack(pady=(10, 15))

# Botón
search_button = ttkbootstrap.Button(
    container,
    text="🔍 Buscar clima",
    command=search,
    bootstyle="info",
    width=22,
    padding=(6, 8)
)
search_button.pack(pady=(0, 20))

# Ubicación
location_label = ttkbootstrap.Label(container, font=("Segoe UI", 22, "bold"), bootstyle="dark")
location_label.pack(pady=(10, 5))

# Icono del clima
icon_label = ttkbootstrap.Label(container)
icon_label.pack(pady=5)

# Clima y temperatura
weather_label = ttkbootstrap.Label(container, font=("Segoe UI", 16), bootstyle="secondary")
weather_label.pack(pady=(5, 10))

print("Aplicación iniciada")
root.mainloop()
