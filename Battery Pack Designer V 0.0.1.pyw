import tkinter as tk  # Biblioteca principală pentru GUI
from tkinter import ttk, messagebox, filedialog, scrolledtext  # Widget-uri avansate și dialoguri
import math  # Funcții matematice (floor, ceil)
import re  # Expresii regulate pentru parsing
import statistics  # Calcule statistice (media)
from itertools import combinations  # Generare combinații
import threading  # Rulare operații în fundal
import os  # Operații cu fișiere și directoare
import sys  # Acces la argumente și calea scriptului
import svgwrite # Folosit la exportul Layout-ului (Bateriei)


# README & MANUAL ======================================================================

def open_readme():
    """Deschide o fereastră secundară cu conținutul README."""
    readme_win = tk.Toplevel(root)                # Creează fereastra copil
    readme_win.title("!!! Readme !!!")           # Setează titlu
    readme_win.geometry("800x400")               # Fixează dimensiunea
    readme_win.configure(bg="#1e1e1e")           # Fundal dark

    txt = tk.Text(
        readme_win,
        wrap=tk.WORD,                            # Întrerupere pe cuvinte
        bg="#1e1e1e", fg="#ffffff",           # Fundal și text alb
        insertbackground="#ffffff"              # Cursor alb
    )
    txt.pack(expand=True, fill=tk.BOTH)           # Umple fereastra

    content = (
"""Battery Pack Calculator v1.0
=============================
This application is designed to assist the user in designing batteries (Li-Ion/LiFePo4 in particular, but also nickel-metal hydride (NiMH) and even lead-acid). The application features a simple calculator for series/parallel configurations wich also computes the total number of cells required, as well as an advanced calculator for batteries made from recycled cells. This advanced calculator pairs the cells (based on their measured capacities, entered into the program) into groups of n/series and n/parallel so that the resulting battery is as balanced as possible in terms of cell capacity.
=================================================================================================
!!! Disclaimer & Limitation of Liability !!!

1 No Warranty:

  This application is provided “as-is,” without any express or implied warranties, including, 
  but not limited to, warranties of merchantability, fitness for a particular purpose, or 
  non- infringement.

2 Use at Your Own Risk:

  Any battery design produced with this application—whether using new cells 
  (simple  series/parallel calculation) or recycled cells (advanced pairing calculation) 
  is  undertaken solely at the user’s own risk. The developer shall not be liable for:

* Inaccurate results due to measurement errors or incorrect input values

* Equipment failures, environmental damage, or accidents

* Loss of data or time caused by software errors

3 Limitation of Liability:

  Under no circumstances will the developer be liable for any indirect, incidental, special,
  punitive, or consequential damages (including, but not limited to, loss of profit, business
  interruption, or loss of information) arising out of or in connection with the use or inability
  to use the application, even if the developer has been advised of the possibility of such
  damages.

4 Safety Warning:

All battery testing and cell handling must be performed in a safe environment, using appropriate protective equipment (e.g., goggles, gloves).

Do not leave overcharged or uneven-capacity cells unattended.

This application does not replace manufacturer recommendations or electrical and thermal safety standards.

5 User Responsibilities

 * Always verify the accuracy of entered values (capacity, voltage, tolerance delta).

 * Comply with applicable laws and regulations for battery design, manufacturing, and recycling.

 * Ensure any practical work is performed by qualified personnel.

6 Intellectual Property:

  All intellectual property rights in the application (source code, interface, documentation)
  belong to the developer. Reproduction, distribution, or modification without written permission
  is prohibited.

7 Changes and Updates:

  The developer reserves the right to modify, suspend, or discontinue any part of the
  application, as well as these disclaimer terms, at any time and without prior notice.

By using this application, you acknowledge that you have read, understood, and agreed to this disclaimer.
================================================================================================
Developer: Nechifor Marian
  Contact: diwhy.engineering.86@gmail.com
  Webpage: https://www.youtube.com/@DIY_Engineering

"""
    )
  # Conținut README prescurtat
    txt.insert(tk.END, content)                   # Afișează conținutul
    txt.config(state=tk.DISABLED)                 # Setează readonly


def open_user_manual():
    """Deschide o fereastră cu manualul de utilizare."""
    manual_win = tk.Toplevel(root)                # Creează fereastră copil
    manual_win.title("User Manual")               # Setează titlu
    manual_win.geometry("550x400")                # Fixează dimensiunea
    manual_win.configure(bg="#1e1e1e")            # Fundal dark

    txt = tk.Text(
        manual_win, wrap=tk.WORD,
        bg="#1e1e1e", fg="#ffffff",
        insertbackground="#ffffff"
    )
    txt.pack(expand=True, fill=tk.BOTH)            # Umple fereastra

    content = (
"""User Manual
===========
1. Fill in the fields in the 'New Cell Battery Calculator' section:
 - Desired Voltage (V)
 - Desired Capacity (mAh)
 - Cell Type (small list with most common cell types/voltages)
 - Cell Capacity (mAh)
 - Press 'Calculate' for SxP configuration
 - Press 'Reset' to clear the fields

2. In the 'Recycled Cell Battery Calculator' section:
 - Enter 'Battery type' (ex. 13S3P)
 - Optional: 'Delta limit' (mAh) (Default Delta is 10% 
   of the average cells capacity)
 - List of capacities (comma-separated)
 - Press 'Calculate' and wait for the animation to stop
 - The detailed result appears in the output area
 - Press 'Save Result' to export a .txt file with 
   the computed cell pairing
 
3. Battery Layout Editor
 - Enter the battery configutation (nSnP)
 - Select layout type (grid or staggered) and press generate
 - If you desire to arrange the cella in a custom manner 
   select "free" option
 - Cells are drawn on two canvases, one is top wiew and the other 
   is bottom wiew (mirror, for convenience)
   The cells are placed on a invisible grid of 
   lines spaced 2x2 pixeli apart
 - Drawing Tabs and moving the cells is done by holding 
   right-click on a cell and then moving it in a desired location
   drawing tabs between the cells is done by left click-ing the 
   free space between the cell number and the cell perimeter
   until the cell number is highlighted and then left-clicking the 
   cell to wich you wish to make connection with

4. Tips:
 - Cell capacities should be close to each other
 - Use delta limit input for fine control of capacity 
   differential, but you may need to
   add more cell capacities in the designated field and
   also be prepared for a longer processing time 
   (5 to 10 minutes, depending on the number of 
   cells and the set Delta)

   === Be SMART And Wear Safety Glasses/Gloves ===
=== And ALWAYS Have A Fire Extinguisher Nearby 🔥🧯==
        
       ⚡Good Luck On Your Battery Project⚡
"""
    )
  # Conținut manual
    txt.insert(tk.END, content)                   # Afișează manual
    txt.config(state=tk.DISABLED)                 # Setează readonly


# ANIMAȚIE ICONURI =========================================================================

def load_icons():
    """Încarcă cadrele animației din folderul 'icons'."""
    imgs = []                                      # Lista pentru imagini
    for i in range(1, 7):                          # 6 cadre
        path = os.path.join(
            os.path.dirname(sys.argv[0]),
            "icons", f"{i}.png"
        )                                         # Construiește calea
        try:
            imgs.append(tk.PhotoImage(file=path)) # Încarcă imaginea
        except Exception:
            imgs.append(None)                     # Dacă lipsește, None
    return imgs                                   # Returnează lista


def cycle_icons():
    """Rulează animația prin schimbarea cadrelor."""
    global animation_id
    if animation_running:
        img = icons_images[icon_index[0]]          # Imaginea curentă
        if img:
            icon_label.config(image=img)           # Schimbă pe label
        icon_index[0] = (icon_index[0] + 1) % len(icons_images)  # Actualizează index
        animation_id = root.after(500, cycle_icons)  # Apel recurent
    else:
        last = icons_images[-1]
        if last:
            icon_label.config(image=last)          # Ultimul cadru


def start_animation():
    """Pornește animația."""
    global animation_running
    animation_running = True                      # Activează flag
    icon_index[0] = 0                             # Reset index
    cycle_icons()                                 # Pornește ciclul


def stop_animation():
    """Oprește animația și anulează apelurile viitoare."""
    global animation_running
    animation_running = False                     # Dezactivează flag
    if animation_id:
        root.after_cancel(animation_id)           # Anulează after
    last = icons_images[-1]
    if last:
        icon_label.config(image=last)             # Setează ultimul cadru


# CALCULATOR SERIE/PARALEL (Simplu) ===================================================================

def calculate_simple():
    """Calculează și afișează SxP pentru celule noi."""
    try:
        V_d = float(entry_voltage.get())          # Tensiune dorită
        C_d = float(entry_capacity.get())         # Capacitate dorită
        C_c = float(entry_cell_cap.get())         # Capacitate celulă
        if V_d <= 0 or C_d <= 0 or C_c <= 0:     # Validare input
            result_simple.set("Error: valori pozitive necesare.")
            return
        # Tensiunea unei celule după chimie
        cell_V = {
            "Li-Ion": 3.7,
            "LiFePo4": 3.2,
            "NIMH": 1.2,
            "Lead Acid": 2.0
        }[cell_type_var.get()]
        # Calc. număr serii (minim eroare)
        rS = V_d / cell_V
        fS, cS = max(1, math.floor(rS)), max(1, math.ceil(rS))
        errS = (abs(fS*cell_V - V_d), abs(cS*cell_V - V_d))
        S = cS if errS[1] < errS[0] else fS
        # Calc. număr paralel (minim eroare)
        rP = C_d / C_c
        fP, cP = max(1, math.floor(rP)), max(1, math.ceil(rP))
        errP = (abs(fP*C_c - C_d), abs(cP*C_c - C_d))
        P = cP if errP[1] <= errP[0] else fP
        total = S * P
        result_simple.set(f"{S}S{P}P   Total cells: {total}")  # Afișare rezultat
    except ValueError:
        result_simple.set("Error: Invalid Input.")          # Eroare conversie


def reset_simple():
    """Resetează câmpurile și rezultatul calculatorului simplu."""
    entry_voltage.delete(0, tk.END)
    entry_capacity.delete(0, tk.END)
    entry_cell_cap.delete(0, tk.END)
    cell_type_combo.current(0)
    result_simple.set("")


# ADVANCED RECYCLED CELL MATCHING =====================================================================

def parse_battery_type(text):
    """Parsează XsYp în (X, Y)."""
    m = re.match(r"(\d+)s(\d+)p", text.lower())
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def suggest_delta_limit(cells):
    """Sugerează delta = 10% din media capacităților."""
    try:
        return int(statistics.mean(cells) * 0.1)
    except:
        return 500


def get_delta_limit():
    """Obține limita delta din input sau sugerează."""
    txt = delta_entry.get().strip()
    if txt:
        try:
            val = int(txt)
            if val > 0:
                return val
        except ValueError:
            messagebox.showwarning("Warning", "Delta invalid, folosesc 10% medie.")
    try:
        caps = list(map(int, cell_text.get("1.0", tk.END).split(",")))
    except:
        caps = []
    return suggest_delta_limit(caps)


def group_cells_balanced(capacities, series, parallel):
    """Grupare greedy echilibrată pe sumă."""
    sorted_caps = sorted(capacities, reverse=True)
    groups = [[] for _ in range(series)]
    sums = [0] * series
    for cap in sorted_caps:
        idx = min(range(series), key=lambda i: (sums[i], len(groups[i]) < parallel))
        if len(groups[idx]) < parallel:
            groups[idx].append(cap)
            sums[idx] += cap
    delta = max(sums) - min(sums)
    used = [c for g in groups for c in g]
    rem = capacities.copy()
    for c in used:
        rem.remove(c)
    return groups, delta, rem


def optimize_best_grouping(capacities, series, parallel, delta_limit):
    """Testează combinații și alege cea mai bună sub delta limit."""
    needed = series * parallel
    best, bd, br = None, None, []
    for combo in combinations(capacities, needed):
        g, d, rem = group_cells_balanced(list(combo), series, parallel)
        if d <= delta_limit:
            return g, d, rem
        if bd is None or d < bd:
            best, bd, br = g, d, rem
    return best, bd, br


def format_groups(groups, remaining, delta):
    """Formatează textul rezultatului, sortând grupurile crescător."""
    sorted_groups = sorted(groups, key=lambda g: sum(g))
    lines = []
    lines.append(f"Grouped cells into {len(sorted_groups)} series of {len(sorted_groups[0])} cells each:")
    for i, g in enumerate(sorted_groups, 1):
        lines.append(f"Group {i:2}: {g} => Total: {sum(g)} mAh")
    lines.append(f"Delta: {delta} mAh")
    if remaining:
        lines.append("Unused cells:")
        lines.append(", ".join(map(str, remaining)))
    return "\n".join(lines)


def calculate_advanced():
    """Procesează și afișează rezultatul grupării avansate."""
    S, P = parse_battery_type(battery_type_entry.get().strip())
    if not S or not P:
        messagebox.showerror("Error", "Format must be nSnP (i.e. 13S3P)")
        stop_animation()
        return
    try:
        caps = list(map(int, cell_text.get("1.0", tk.END).split(",")))
    except ValueError:
        messagebox.showerror("Error", "Lista de celule invalidă")
        stop_animation()
        return
    if len(caps) < S * P:
        messagebox.showerror("Error", f"Trebuie cel puțin {S*P} celule")
        stop_animation()
        return
    dl = get_delta_limit()
    g, d, rem = optimize_best_grouping(caps, S, P, dl)
    if d > dl:
        messagebox.showwarning("Warning", f"Delta minim găsit: {d} mAh, depășește limita {dl} mAh")
    res = format_groups(g, rem, d)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, res)
    output_text.config(state=tk.DISABLED)
    save_btn.config(state=tk.NORMAL)
    stop_animation()


def on_calculate_advanced():
    """Pregătește UI și lansează calculul în thread."""
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    save_btn.config(state=tk.DISABLED)
    start_animation()
    threading.Thread(target=calculate_advanced, daemon=True).start()


def save_advanced_result():
    """Salvează rezultatul într-un fișier .txt."""
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text files","*.txt")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"Rezultat salvat în: {path}")


def load_from_file():
    """Încarcă capacități dintr-un fișier în widgetul de text."""
    file_path = filedialog.askopenfilename(
        title="Selectează fișierul cu valori",
        filetypes=[("Text files", "*.txt")]
    )
    if not file_path:
        return
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read().strip()
        cell_text.delete("1.0", tk.END)
        cell_text.insert(tk.END, data)
    except Exception as e:
        messagebox.showerror("Eroare", f"Nu am putut citi fișierul:\n{e}")


# CONFIGURARE FEREASTRĂ PRINCIPALĂ ȘI LAYOUT =================================================================

root = tk.Tk()  # Creează fereastra principală
root.title("Battery Pack Designer V0.0.1")  # Setează titlul
# Dimensiunile dorite pentru fereastra ta
window_width = 1445
window_height = 773

# Obținem rezoluția ecranului (lățime și înălțime)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculăm coordonatele X și Y pentru colțul stânga-sus, astfel încât fereastra să fie la mijloc
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# Setăm geometria folosind formatul: "Lățime x Înălțime + X + Y"
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.configure(bg="#1e1e1e")  # Fundal dark

style = ttk.Style()
style.theme_use("clam")  # Tema Grafica
style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI",10))
style.configure("TButton", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI",10), padding=5)
style.map("TButton", background=[("active","#1e1e1e")], foreground=[("pressed","#ffffff")])
style.configure("TEntry", fieldbackground="#1e1e1e", foreground="#ffffff")
style.configure("TCombobox", fieldbackground="#1e1e1e", foreground="#2e2e2e")

icons_images = load_icons()  # Încarcă animație iconițe
icon_index = [0]  # Index pentru animație
animation_running = False  # Flag animație
animation_id = None  # ID apel after

icon_label = tk.Label(root, bg="#1e1e1e")  # Label pentru animație
icon_label.place(x=240, y=8, width=256, height=256)
if icons_images and icons_images[0]:
    icon_label.config(image=icons_images[0])  # Imagine inițială

# ==== FRAME: New Cells Battery Calculator ====

simple_frame = tk.LabelFrame(
    root, text=" New Cells Battery Calculator ",
    fg="white", bg="#1e1e1e", font=("Segoe UI",10,"bold")
)
simple_frame.place(x=6, y=0, width=280, height=260)

ttk.Label(simple_frame, text="Desired Voltage (V)",).place(x=10, y=10)   # Eticheta tensiune
entry_voltage = ttk.Entry(simple_frame, width=15)                     # Câmp input tensiune
entry_voltage.place(x=160, y=10)

ttk.Label(simple_frame, text="Desired Capacity (mAh)").place(x=10, y=45)
entry_capacity = ttk.Entry(simple_frame, width=15)
entry_capacity.place(x=160, y=45)

ttk.Label(simple_frame, text="Cell Type (Chemistry)").place(x=10, y=80)
cell_type_var = tk.StringVar()                                         # Variabilă asociată combobox
cell_type_combo = ttk.Combobox(
    simple_frame, textvariable=cell_type_var,
    values=("Li-Ion","LiFePo4","NIMH","Lead Acid"), state="readonly", width=13
)
cell_type_combo.current(0)
cell_type_combo.place(x=160, y=80)

ttk.Label(simple_frame, text="Cell Capacity (mAh)").place(x=10, y=115)
entry_cell_cap = ttk.Entry(simple_frame, width=15)
entry_cell_cap.place(x=160, y=115)

btn_calc_simple = ttk.Button(simple_frame, text="Calculate", command=calculate_simple)  # Buton calcul
btn_calc_simple.place(x=20, y=155, width=100)
btn_reset_simple = ttk.Button(simple_frame, text="Reset", command=reset_simple)        # Buton reset
btn_reset_simple.place(x=158, y=155, width=100)

result_simple = tk.StringVar()                                          # Variabilă pentru rezultat
ttk.Label(
    simple_frame, textvariable=result_simple,
    font=("Segoe UI",11,"bold")
).place(x=60, y=200)                                                     # Afișare rezultat

# ==== FRAME: Recycled Cells Battery Calculator ====

adv_frame = tk.LabelFrame(
    root, text=" Recycled Cells Battery Calculator ",
    fg="white", bg="#1e1e1e", font=("Segoe UI",10,"bold")
)
adv_frame.place(x=6, y=260, width=562, height=506)

ttk.Label(adv_frame, text="Battery Type (nSnP) ----------------").place(x=10, y=10)
battery_type_entry = ttk.Entry(adv_frame, width=7)  # Input tip baterie
battery_type_entry.place(x=210, y=10)

ttk.Label(adv_frame, text="Delta limit (mAh, optional) --------").place(x=10, y=40)
delta_entry = ttk.Entry(adv_frame, width=7)        # Input delta limit
delta_entry.place(x=210, y=40)

ttk.Label(adv_frame, text="Cell capacities (comma-separated)").place(x=10, y=70)
cell_text = scrolledtext.ScrolledText(
    adv_frame, width=74, height=5,
    bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
    font=("Segoe UI",10)
)
cell_text.place(x=10, y=90)                                # Zona text pentru liste

btn_calc_adv = ttk.Button(adv_frame, text="Calculate", command=on_calculate_advanced)  # Buton avansat
btn_calc_adv.place(x=305, y=40, width=100)
save_btn = ttk.Button(adv_frame, text="Save Result", command=save_advanced_result, state=tk.DISABLED)  # Buton salvare
save_btn.place(x=430, y=20, width=100)

ttk.Label(adv_frame, text="Result:").place(x=10, y=180)   # Etichetă rezultat
output_text = scrolledtext.ScrolledText(
    adv_frame, width=74, height=16,
    bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
    font=("Segoe UI",10), state=tk.DISABLED
)
output_text.place(x=10, y=200)                              # Afișare rezultat

load_btn = ttk.Button(adv_frame, text="Load File", command=load_from_file)  # Load din fișier
load_btn.place(x=305, y=2, width=100)

# BUTOANE README & MANUAL
readme_btn = ttk.Button(root, text="Readme", command=open_readme)
readme_btn.place(x=440, y=90, width=100)
manual_btn = ttk.Button(root, text="User Manual", command=open_user_manual)
manual_btn.place(x=440, y=175, width=100)
 

# ================ BATTERY LAYOUT EDITOR INTEGRAT ======================
layout_frame = tk.LabelFrame(root, text=" Battery Layout Editor ", fg="white", bg="#1e1e1e", font=("Segoe UI",10,"bold"))
layout_frame.place(x=575, y=0, width=864, height=766)

class EmbeddedBatteryLayout(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#1e1e1e')
        # Ne asigurăm că acest cadru ocupă tot spațiul oferit de layout_frame
        self.place(x=0, y=0, relwidth=1, relheight=1)

        # Stiluri interfață [cite: 53, 54]
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background='#1e1e1e', foreground='#f0f0f0', fieldbackground='#444444')

        # Variabile stare (Corectate pentru a evita SyntaxError) [cite: 54, 55, 56]
        self.mm_to_px = 3
        self.d = 18 * self.mm_to_px
        self.strip_width = 9 * self.mm_to_px
        self.type_var = tk.StringVar()
        self.mode_var = tk.StringVar(value='grid')
        self.status_var = tk.StringVar(value='Ready')
        
        self.cells = {}
        self.texts = {}
        self.positions = {}
        self.connections_top = []
        self.connections_bottom = []
        self.selected_top = None
        self.selected_bottom = None
        self.drag_data = {'item': None, 'orig': (0, 0), 'x': 0, 'y': 0}
        self.history = []

        # --- GUI în coordonate FIXE (Margini 6px) --- [cite: 56, 58]
        
        # Bara de unelte (Toolbar)
        ttk.Label(self, text='Battery Type (nSnP)').place(x=244, y=7)
        ttk.Entry(self, width=7, textvariable=self.type_var).place(x=370, y=8)
        
        ttk.Radiobutton(self, text='Grid', variable=self.mode_var, value='grid').place(x=480, y=8)
        ttk.Radiobutton(self, text='Staggered', variable=self.mode_var, value='staggered').place(x=530, y=8)
        ttk.Radiobutton(self, text='Free', variable=self.mode_var, value='free').place(x=430, y=8)

        # Butoane Acțiune [cite: 56, 57]
        ttk.Button(self, text='Generate', command=self.generate_grid).place(x=610, y=0, width=80)
        ttk.Button(self, text='Undo', command=self.undo).place(x=699, y=0, width=65)
        ttk.Button(self, text='Save SVG', command=self.export_svg).place(x=773, y=0, width=80)

        # Canvas-uri (Lățime: 800 - 12 = 788px) [cite: 58]
        ttk.Label(self, text='Top View').place(x=6, y=20)
        self.canvas_top = tk.Canvas(self, bg='#1e1e1e', highlightthickness=1, highlightbackground="#333333")
        self.canvas_top.place(x=8, y=43, width=845, height=330)

        ttk.Label(self, text='Bottom View (Mirror)').place(x=6, y=383)
        self.canvas_bottom = tk.Canvas(self, bg='#1e1e1e', highlightthickness=1, highlightbackground="#333333")
        self.canvas_bottom.place(x=8, y=406, width=845, height=330)

        # Status Bar [cite: 58]
        self.status_lbl = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w')
        self.status_lbl.place(x=0, y=745, relwidth=1)

        # Bindings [cite: 59]
        self.canvas_top.bind('<ButtonPress-3>', self.on_start_drag_top)
        self.canvas_top.bind('<B3-Motion>', self.on_drag_top)
        self.canvas_top.bind('<ButtonRelease-3>', self.on_drop_top)
        self.canvas_top.bind('<Button-1>', self.on_canvas_click_top)
        self.canvas_bottom.bind('<Button-1>', self.on_canvas_click_bottom)
   
    def parse_config(self, config_str):
        """
        Parsează string-ul de configurare nSnP și returnează (rows, cols).
        Dacă formatul e invalid, apare un dialog de eroare.
        """
        m = re.match(r"(\d+)[sS](\d+)[pP]", config_str)
        if not m:
            messagebox.showerror('Format error','Format must be nSnP (i.e. 13S3P)')
            return None,None
        return int(m.group(2)), int(m.group(1))

    def generate_grid(self):
        """
        Generează layout-ul conform configurației.
        Șterge canvas-urile, reconstruieste poziții și desenează celulele.
        """
        self.status_var.set('Generating layout...')
        self.update_idletasks()
        for c in (self.canvas_top, self.canvas_bottom):
            c.delete('all')
        self.cells.clear(); self.texts.clear(); self.positions.clear()
        self.connections_top.clear(); self.connections_bottom.clear()
        self.history.clear(); self.selected_top=None; self.selected_bottom=None

        rows,cols = self.parse_config(self.type_var.get().strip())
        if not rows or not cols:
            self.status_var.set('Invalid config')
            return
        mode = self.mode_var.get()
        sin60 = math.sin(math.pi/3)
        step_x = self.d
        step_y = self.d*(sin60 if mode=='staggered' else 1)
        off = self.d/2
        h_top = self.canvas_top.winfo_height()
        idx = 1
        for r in range(rows):
            for c in range(cols):
                x = c*step_x + off + (step_x/2 if mode=='staggered' and r%2 else 0)
                y = r*step_y + off
                oval_color='#3e3e3e'; text_color='#f0f0f0'
                oid = self.canvas_top.create_oval(
                    x-self.d/2, y-self.d/2, x+self.d/2, y+self.d/2,
                    fill=oval_color, outline=text_color)
                tid = self.canvas_top.create_text(x, y, text=str(idx), font=('Arial',8), fill=text_color)
                self.cells[oid] = idx
                self.texts[idx] = tid
                self.positions[idx] = (x, y)
                # desenă conexiunile deja existente pe top ca să fie vizibile după generare
                if self.connections_top:
                    self.redraw_strips(self.canvas_top, self.connections_top)
                # bottom oglindit
                yb = h_top - y
                self.canvas_bottom.create_oval(
                    x-self.d/2, yb-self.d/2, x+self.d/2, yb+self.d/2,
                    fill=oval_color, outline=text_color)
                self.canvas_bottom.create_text(x, yb, text=str(idx), font=('Arial',8), fill=text_color)
                if self.connections_bottom:
                    self.redraw_strips(self.canvas_bottom, self.connections_bottom, mirror=True)
                idx += 1
        self.status_var.set('Layout generated')

    def undo(self):
        """
        Revine la ultima acțiune (move/connection).
        """
        if not self.history:
            self.status_var.set('Nothing to undo')
            return
        action = self.history.pop()
        typ = action[0]
        if typ=='move':
            _, idx, old = action
            x0, y0 = old
            for oid,i in self.cells.items():
                if i==idx:
                    self.canvas_top.coords(oid, x0-self.d/2, y0-self.d/2, x0+self.d/2, y0+self.d/2)
                    break
            self.canvas_top.coords(self.texts[idx], x0, y0)
            self.positions[idx] = (x0, y0)
            self.redraw_mirror()
        elif typ=='connect_top':
            self.connections_top.pop()
            self.redraw_strips(self.canvas_top, self.connections_top)
        elif typ=='connect_bottom':
            self.connections_bottom.pop()
            self.redraw_strips(self.canvas_bottom, self.connections_bottom, mirror=True)
        self.status_var.set('Undo performed')

    def on_canvas_click_top(self, event):
        """
        Selectează/conectează celule în top view la click stânga.
        """
        hit = self.canvas_top.find_closest(event.x, event.y)
        if not hit: return
        oid = hit[0]
        if oid not in self.cells: return
        idx = self.cells[oid]
        if self.selected_top is None:
            self.selected_top = idx
            self.canvas_top.itemconfigure(self.texts[idx], fill='#ff8080')
            self.status_var.set(f'Selected top {idx}')
        else:
            prev = self.selected_top
            self.canvas_top.itemconfigure(self.texts[prev], fill='#f0f0f0')
            x1, y1 = self.positions[prev]
            x2, y2 = self.positions[idx]
            # desenăm conexiunea imediat
            self.draw_strip(self.canvas_top, x1, y1, x2, y2)
            self.connections_top.append((prev, idx))
            self.history.append(('connect_top', prev, idx))
            self.selected_top = None
            self.status_var.set(f'Connected top {prev}->{idx}')

    def on_canvas_click_bottom(self, event):
        """
        Selectează/conectează celule în bottom view la click stânga.
        """
        hit = self.canvas_bottom.find_closest(event.x, event.y)
        if not hit: return
        x, y = event.x, event.y
        h_top = self.canvas_top.winfo_height()
        idx = None
        for i, (cx, cy) in self.positions.items():
            if abs(cx-x)<self.d/2 and abs(h_top-cy-y)<self.d/2:
                idx = i
                break
        if idx is None: return
        if self.selected_bottom is None:
            self.selected_bottom = idx
            self.status_var.set(f'Selected bottom {idx}')
        else:
            prev = self.selected_bottom
            x1, y1 = self.positions[prev]; y1b = h_top - y1
            x2, y2 = self.positions[idx]; y2b = h_top - y2
            # desenăm conexiunea imediat
            self.draw_strip(self.canvas_bottom, x1, y1b, x2, y2b)
            self.connections_bottom.append((prev, idx))
            self.history.append(('connect_bottom', prev, idx))
            self.selected_bottom = None
            self.status_var.set(f'Connected bottom {prev}->{idx}')

    def on_start_drag_top(self, event):
        """
        Începe operația de drag&drop pentru mod free (click dreapta).
        """
        if self.mode_var.get()!='free': return
        hit = self.canvas_top.find_closest(event.x, event.y)
        if not hit: return
        oid = hit[0]
        if oid in self.cells:
            idx = self.cells[oid]
            self.drag_data = {'item': oid, 'orig': self.positions[idx], 'x': event.x, 'y': event.y}
            self.status_var.set(f'Dragging {idx}')

    def on_drag_top(self, event):
        """
        După mutare mouse cu butonul 3 apăsat, mută oval și text.
        """
        if self.mode_var.get()!='free': return
        d = self.drag_data; oid = d.get('item')
        if not oid: return
        dx, dy = event.x - d['x'], event.y - d['y']
        self.canvas_top.move(oid, dx, dy)
        self.canvas_top.move(self.texts[self.cells[oid]], dx, dy)
        d['x'], d['y'] = event.x, event.y

    def on_drop_top(self, event):
        """
        La eliberare buton 3, fixează poziția pe grilă, verifică overlap.
        """
        if self.mode_var.get()!='free': return
        d = self.drag_data; oid = d.get('item')
        if not oid: return
        idx = self.cells[oid]; old = d['orig']
        x1, y1, x2, y2 = self.canvas_top.coords(oid)
        cx, cy = (x1+x2)/2, (y1+y2)/2
        sx, sy = round(cx/self.mm_to_px)*self.mm_to_px, round(cy/self.mm_to_px)*self.mm_to_px
        overlap = False
        for j, (jx, jy) in self.positions.items():
            if j==idx: continue
            if math.hypot(sx-jx, sy-jy) < self.d:
                overlap = True
                break
        if overlap:
            sx, sy = old
        self.history.append(('move', idx, old))
        dx, dy = sx-cx, sy-cy
        self.canvas_top.move(oid, dx, dy)
        self.canvas_top.move(self.texts[idx], dx, dy)
        self.positions[idx] = (sx, sy)
        self.redraw_mirror()
        self.status_var.set(f'Placed {idx} at {sx/self.mm_to_px}mm,{sy/self.mm_to_px}mm')
        self.drag_data = {}

    def redraw_mirror(self):
        """
        Redesenare completă a bottom view în oglindă pe baza pozițiilor curente.
        """
        self.canvas_bottom.delete('all')
        h_top = self.canvas_top.winfo_height()
        for i, (cx, cy) in self.positions.items():
            yb = h_top - cy
            self.canvas_bottom.create_oval(
                cx-self.d/2, yb-self.d/2, cx+self.d/2, yb+self.d/2,
                fill='#3e3e3e', outline='#f0f0f0')
            self.canvas_bottom.create_text(cx, yb, text=str(i), font=('Arial',8), fill='#f0f0f0')
        self.redraw_strips(self.canvas_bottom, self.connections_bottom, mirror=True)

    def redraw_strips(self, canvas, conns, mirror=False):
        """
        Desenează benzile de legătură pe canvas-ul dat (top/bottom).
        mirror=True face oglindirea pe verticală.
        """
        canvas.delete('strip')
        h_top = self.canvas_top.winfo_height()
        for prev, idx in conns:
            x1, y1 = self.positions[prev]; x2, y2 = self.positions[idx]
            if mirror:
                y1 = h_top - y1
                y2 = h_top - y2
            canvas.create_line(
                x1, y1, x2, y2,
                fill='#f0f0f0',
                width=self.strip_width,
                capstyle=tk.ROUND,
                tags='strip')

    def draw_strip(self, canvas, x1, y1, x2, y2):
        """
        Adaugă o linie de legătură nouă pe canvas-ul specificat.
        Folosit la conectare manuală (click între două celule).
        """
        canvas.create_line(
            x1, y1, x2, y2,
            fill='#f0f0f0',
            width=self.strip_width,
            capstyle=tk.ROUND,
            tags='strip')

    def export_svg(self):
        """
        Exportă întreg layout-ul în fișier SVG, fidel la ecran:
          - include fundalul
          - păstrează dimensiune pixeli și capete rotunde
          - desenează întâi cercurile și textul,
            apoi benzile, pentru ca conexiunile să fie suprapuse peste celule
        """
        if not self.positions:
            messagebox.showwarning('No layout','Generate first')
            return

        fp = filedialog.asksaveasfilename(defaultextension='.svg', filetypes=[('SVG','.svg')])
        if not fp:
            return

        w = self.canvas_top.winfo_width()
        h = self.canvas_top.winfo_height()
        H = h * 2

        dwg = svgwrite.Drawing(fp, size=(f'{w}px', f'{H}px'))

        bg = self.canvas_top['bg']
        dwg.add(dwg.rect(insert=(0,0), size=(w,H), fill=bg))

        # desenăm cercuri și text mai întâi
        for idx,(cx,cy) in self.positions.items():
            dwg.add(dwg.circle(center=(cx,cy), r=self.d/2, fill='#3e3e3e', stroke='white'))
            dwg.add(dwg.text(str(idx), insert=(cx,cy+4), text_anchor='middle', font_size='8px', fill='white'))
            yb = H-cy
            dwg.add(dwg.circle(center=(cx,yb), r=self.d/2, fill='#3e3e3e', stroke='white'))
            dwg.add(dwg.text(str(idx), insert=(cx,yb+4), text_anchor='middle', font_size='8px', fill='white'))

        # apoi benzile
        for conns, mirror in [(self.connections_top, False),(self.connections_bottom, True)]:
            for i1,i2 in conns:
                x1,y1 = self.positions[i1]; x2,y2 = self.positions[i2]
                if mirror:
                    y1 = H-y1; y2 = H-y2
                dwg.add(dwg.line(start=(x1,y1), end=(x2,y2), stroke='white', **{'stroke-width': f'{self.strip_width}px', 'stroke-linecap':'round', 'stroke-linejoin':'round'}))

        dwg.save()
        self.status_var.set(f'SVG salvat în {fp}')


# Instanțiere
embedded = EmbeddedBatteryLayout(layout_frame)

root.mainloop()
