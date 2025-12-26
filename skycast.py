
import tkinter as tk
from tkinter import ttk, messagebox
import requests, geocoder, datetime
from PIL import Image, ImageTk, ImageFilter

API_KEY = "0f11d9bc5e16c8705dd4f8812b06bb1f"  # Add your API key here
FONT = "Segoe UI"

ICON = {"Clear":"☀","Clouds":"☁","Rain":"🌧","Mist":"🌫","Smoke":"💨","Haze":"🌫","Snow":"❄"}

def fetch(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    return data['list'][::8]

def detect():
    g = geocoder.ip('me')
    if g.city: city_var.set(g.city)

def get_weather():
    city = city_var.get()
    d = fetch(city)
    f = forecast(city)
    if str(d.get("cod"))=="200":
        show_weather(d,f)
    else:
        messagebox.showerror("Error","City Not Found")

def show_weather(d,fdata):
    win = tk.Toplevel(root)
    win.state("zoomed")

    W,H = win.winfo_screenwidth(), win.winfo_screenheight()
    bg = Image.open("clouds.jpg").resize((W,H))
    bgp = ImageTk.PhotoImage(bg)
    tk.Label(win,image=bgp).place(relwidth=1,relheight=1)
    win.bg=bgp

    card_w,card_h = 580,560
    x,y = (W-card_w)//2+50,(H-card_h)//2-40
    glass = bg.crop((x,y,x+card_w,y+card_h)).filter(ImageFilter.GaussianBlur(30))
    # Enhanced overlay with better contrast for text visibility
    overlay = Image.new("RGBA",glass.size,(255,255,255,220))  # Changed to white with high opacity
    glass = Image.alpha_composite(glass.convert("RGBA"),overlay)
    gp = ImageTk.PhotoImage(glass)

    card = tk.Label(win,image=gp)
    card.image=gp
    card.place(x=x,y=y)

    city = d["name"]
    temp = round(d["main"]["temp"])
    desc = d["weather"][0]["main"]

    # Enhanced text colors for better visibility on white glass
    tk.Label(card,text=city.upper(),fg="#1e3a8a",font=(FONT,28,"bold")).pack(pady=(35,5))
    tk.Label(card,text=ICON.get(desc,"🌡"),fg="#0f172a",font=(FONT,65)).pack(pady=5)
    tk.Label(card,text=f"{temp}°C",fg="#1e40af",font=(FONT,62,"bold")).pack(pady=5)
    tk.Label(card,text=d["weather"][0]["description"].title(),fg="#334155",font=(FONT,16,"bold")).pack(pady=5)

    # Humidity and Wind in one line
    details_frame = tk.Frame(card, bg=card['bg'])
    details_frame.pack(pady=(22,5))
    
    tk.Label(details_frame,text=f"💧 Humidity: {d['main']['humidity']}%",fg="#1e40af",font=(FONT,17,"bold")).pack(side='left', padx=15)
    tk.Label(details_frame,text=f"🌬 Wind: {d['wind']['speed']} m/s",fg="#1e40af",font=(FONT,17,"bold")).pack(side='left', padx=15)

    fbox = tk.Frame(win,bg="")
    fbox.place(relx=0.5,rely=0.88,anchor="center")

    for day in fdata[:5]:
        # Enhanced forecast cards with better visibility
        fcard = tk.Frame(fbox,bg="#ffffff",padx=20,pady=14,highlightbackground="#3b82f6",highlightthickness=2)
        fcard.pack(side="left",padx=12)
        dt = datetime.datetime.fromtimestamp(day["dt"]).strftime("%a").upper()
        tk.Label(fcard,text=dt,fg="#475569",bg="#ffffff",font=(FONT,12,"bold")).pack(pady=(2,5))
        tk.Label(fcard,text=ICON.get(day["weather"][0]["main"],"☁"),fg="#1e40af",bg="#ffffff",font=(FONT,26)).pack(pady=5)
        tk.Label(fcard,text=f"{round(day['main']['temp'])}°C",fg="#1e3a8a",bg="#ffffff",font=(FONT,14,"bold")).pack(pady=(5,2))

root = tk.Tk()
root.title("SkyCast")
root.state("zoomed")

W,H = root.winfo_screenwidth(), root.winfo_screenheight()
city_var = tk.StringVar(value="Mumbai")

bg = Image.open("clouds.jpg").resize((W,H))
bgp = ImageTk.PhotoImage(bg)
tk.Label(root,image=bgp).place(relwidth=1,relheight=1)
root.bg=bgp

card_w,card_h=450,480
x,y=(W-card_w)//2+90,(H-card_h)//2
glass = bg.crop((x,y,x+card_w,y+card_h)).filter(ImageFilter.GaussianBlur(30))
# Enhanced overlay for better text visibility on main page
overlay = Image.new("RGBA",glass.size,(255,255,255,230))  # Changed to white with high opacity
glass = Image.alpha_composite(glass.convert("RGBA"),overlay)
gp = ImageTk.PhotoImage(glass)

card = tk.Label(root,image=gp)
card.image=gp
card.place(x=x,y=y)

# Enhanced colors for better visibility
tk.Label(card,text="🌦 SKYCAST",fg="#1e3a8a",font=(FONT,36,"bold")).pack(pady=(45,8))
tk.Label(card,text="Premium Weather Forecasting",fg="#334155",font=(FONT,13,"bold")).pack(pady=(0,35))

cities=["Mumbai","Delhi","Bengaluru","Chennai","Kolkata","Hyderabad","Pune"]

# Styled combobox with better visibility
style = ttk.Style()
style.theme_use('clam')
style.configure('Custom.TCombobox', 
                fieldbackground='#e0f2fe',
                background='#3b82f6',
                foreground='#0f172a',
                arrowcolor='#1e40af',
                bordercolor='#3b82f6')
style.map('Custom.TCombobox', 
          fieldbackground=[('readonly','#e0f2fe')],
          selectbackground=[('readonly', '#bfdbfe')],
          selectforeground=[('readonly', '#1e3a8a')])

box = ttk.Combobox(card,values=cities,textvariable=city_var,font=(FONT,15),width=24,style='Custom.TCombobox',state='readonly')
box.pack(pady=15)

# Enhanced buttons with better colors
tk.Button(card,text="📍 Auto Detect My City",command=detect,bg="#2563eb",fg="white",font=(FONT,13,"bold"),relief="flat",width=26,cursor="hand2",activebackground="#1e40af").pack(pady=12)
tk.Button(card,text="🌤 Get Weather Report",command=get_weather,bg="#0ea5e9",fg="white",font=(FONT,13,"bold"),relief="flat",width=26,cursor="hand2",activebackground="#0284c7").pack(pady=10)

root.mainloop()