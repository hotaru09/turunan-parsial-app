# Aplikasi EOQ (Economic Order Quantity) 
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# Fungsi perhitungan EOQ
def hitung_eoq():
    try:
        D = float(entry_permintaan.get())
        S = float(entry_biaya_pesan.get())
        H = float(entry_biaya_simpan.get())

        EOQ = math.sqrt((2 * D * S) / H)
        N = D / EOQ
        TC = (N * S) + (EOQ / 2 * H)

        tampilkan_grafik(D, S, H, EOQ, N, TC)

    except Exception as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi reset
def reset_form():
    entry_permintaan.delete(0, tk.END)
    entry_biaya_pesan.delete(0, tk.END)
    entry_biaya_simpan.delete(0, tk.END)
    fig.clear()
    canvas.draw()

# Grafik 3D EOQ dengan penjelasan

def tampilkan_grafik(D, S, H, EOQ, N, TC):
    fig.clear()
    ax = fig.add_subplot(111, projection='3d')
    q = np.linspace(1, 2*EOQ, 30)
    s = np.linspace(1, 2*S, 30)
    Q, S_grid = np.meshgrid(q, s)
    TC_grid = (D / Q) * S_grid + (Q / 2) * H

    ax.plot_surface(Q, S_grid, TC_grid, cmap='coolwarm', edgecolor='k', alpha=0.9)
    ax.set_title("Total Cost vs Order Quantity & Biaya Pemesanan", color='white', pad=10)
    ax.set_xlabel("Jumlah Pemesanan (Q)", color='white', labelpad=10)
    ax.set_ylabel("Biaya Pemesanan (S)", color='white', labelpad=10)
    ax.set_zlabel("Total Biaya", color='white', labelpad=10)

    # Teks penjelasan di dalam grafik
    info_text = f"EOQ: {EOQ:.2f}\nTotal Biaya: Rp {TC:,.2f}\nPemesanan/Tahun: {N:.2f}"
    ax.text2D(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=11, color='black', bbox=dict(facecolor='white', alpha=0.7))

    fig.tight_layout()
    fig.patch.set_facecolor('#2b2b2b')
    canvas.draw()

# GUI Utama
app = tk.Tk()
app.title("Kalkulator EOQ - Scroll Responsif")
app.state('zoomed')
app.configure(bg='#2b2b2b')

# Scrollable canvas (dua arah)
main_canvas = tk.Canvas(app, bg='#2b2b2b', highlightthickness=0)
scrollbar_y = tk.Scrollbar(app, orient="vertical", command=main_canvas.yview)
scrollbar_x = tk.Scrollbar(app, orient="horizontal", command=main_canvas.xview)
main_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")
main_canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(main_canvas, bg='#2b2b2b')
main_canvas.create_window((0, 0), window=content, anchor='nw')
content.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

# Frame tengah
center_frame = tk.Frame(content, bg='#2b2b2b')
center_frame.grid(row=0, column=0, padx=app.winfo_screenwidth() // 4)

# Judul
judul = tk.Label(center_frame, text="Simulasi EOQ (Economic Order Quantity)", font=("Segoe UI", 18, "bold"), bg="#2b2b2b", fg="white")
judul.pack(pady=20)

# Frame input
form_frame = tk.Frame(center_frame, bg='#1e1e1e', padx=40, pady=30)
form_frame.pack(pady=10)

fields = [
    ("Permintaan Tahunan (unit):", 'entry_permintaan'),
    ("Biaya Pemesanan per Order (Rp):", 'entry_biaya_pesan'),
    ("Biaya Penyimpanan/unit/tahun (Rp):", 'entry_biaya_simpan')
]

entries = {}

for text, key in fields:
    row = tk.Frame(form_frame, bg='#1e1e1e')
    row.pack(pady=10)
    lbl = tk.Label(row, text=text, font=("Segoe UI", 12), bg='#1e1e1e', fg='white')
    lbl.pack(side="left", padx=10)
    ent = tk.Entry(row, font=("Segoe UI", 12), width=30, bg="#ffffff", fg="black")
    ent.pack(side="left")
    entries[key] = ent

entry_permintaan = entries['entry_permintaan']
entry_biaya_pesan = entries['entry_biaya_pesan']
entry_biaya_simpan = entries['entry_biaya_simpan']

# Tombol
btn_frame = tk.Frame(center_frame, bg="#2b2b2b")
btn_frame.pack(pady=20)
btn_hitung = tk.Button(btn_frame, text="Hitung EOQ", command=hitung_eoq, font=("Segoe UI", 12), bg="#2a9d8f", fg="white", padx=10)
btn_hitung.pack(side="left", padx=10)
btn_reset = tk.Button(btn_frame, text="Reset", command=reset_form, font=("Segoe UI", 12), bg="#e76f51", fg="white", padx=10)
btn_reset.pack(side="left", padx=10)

# Grafik diperbesar
fig = plt.figure(figsize=(10, 7))
canvas = FigureCanvasTkAgg(fig, master=center_frame)
canvas.get_tk_widget().pack(pady=20)

# Scroll Mouse
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def _on_shift_mousewheel(event):
    main_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
main_canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

app.mainloop()
