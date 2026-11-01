
import tkinter as tk
from tkinter import ttk, messagebox

# =====================================
# 1. KONFIGURASI APLIKASI
# =====================================

root = tk.Tk()
root.title("Formulir Identitas Mahasiswa")
root.geometry("700x800")
root.resizable(False, False)

# Warna aplikasi
BG = "#EEF3F8"
NAVY = "#183B56"
BLUE = "#2878A8"
LIGHT_BLUE = "#E5F1F8"
WHITE = "#FFFFFF"
TEXT = "#263746"
GRAY = "#718096"
RED = "#C0392B"

root.configure(bg=BG)

root.grid_columnconfigure(0, weight=1)

# =====================================
# 2. STYLE COMBOBOX
# =====================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Custom.TCombobox",
    fieldbackground=WHITE,
    background=WHITE,
    foreground=TEXT,
    padding=7,
    font=("Arial", 10)
)

# =====================================
# 3. FUNGSI SIMPAN
# =====================================

def simpan():

    nama_value = entry_nama.get().strip()
    nim_value = entry_nim.get().strip()
    gender_value = gender.get()
    prodi_value = combo_prodi.get()
    semester_value = combo_semester.get()
    alamat_value = text_alamat.get("1.0", tk.END).strip()

    # Validasi Nama
    if nama_value == "":
        messagebox.showwarning(
            "Peringatan",
            "Nama tidak boleh kosong!"
        )
        entry_nama.focus()
        return

    # Validasi NIM
    if nim_value == "":
        messagebox.showwarning(
            "Peringatan",
            "NIM tidak boleh kosong!"
        )
        entry_nim.focus()
        return

    if not nim_value.isdigit():
        messagebox.showwarning(
            "Peringatan",
            "NIM harus berupa angka!"
        )
        entry_nim.focus()
        return

    # Validasi Jenis Kelamin
    if gender_value == "":
        messagebox.showwarning(
            "Peringatan",
            "Silakan pilih jenis kelamin!"
        )
        return

    # Validasi Program Studi
    if prodi_value == "":
        messagebox.showwarning(
            "Peringatan",
            "Silakan pilih program studi!"
        )
        combo_prodi.focus()
        return

    # Validasi Semester
    if semester_value == "":
        messagebox.showwarning(
            "Peringatan",
            "Silakan pilih semester!"
        )
        combo_semester.focus()
        return

    # Validasi Alamat
    if alamat_value == "":
        messagebox.showwarning(
            "Peringatan",
            "Alamat tidak boleh kosong!"
        )
        text_alamat.focus()
        return

    # Menampilkan hasil identitas
    hasil.config(
        text=(
            f"Nama             : {nama_value}\n"
            f"NIM              : {nim_value}\n"
            f"Jenis Kelamin    : {gender_value}\n"
            f"Program Studi    : {prodi_value}\n"
            f"Semester         : {semester_value}\n"
            f"Alamat           : {alamat_value}"
        ),
        fg=TEXT
    )

    messagebox.showinfo(
        "Berhasil",
        "Data identitas mahasiswa berhasil disimpan!"
    )


# =====================================
# 4. FUNGSI RESET
# =====================================

def reset():

    konfirmasi = messagebox.askyesno(
        "Konfirmasi Reset",
        "Apakah Anda yakin ingin mengosongkan formulir?"
    )

    if konfirmasi:

        entry_nama.delete(0, tk.END)
        entry_nim.delete(0, tk.END)

        gender.set("")
        combo_prodi.set("")
        combo_semester.set("")

        text_alamat.delete("1.0", tk.END)

        hasil.config(
            text="Data identitas akan ditampilkan di sini.",
            fg=GRAY
        )

        entry_nama.focus()


# =====================================
# 5. FUNGSI KELUAR
# =====================================

def keluar():

    konfirmasi = messagebox.askyesno(
        "Konfirmasi Keluar",
        "Apakah Anda yakin ingin keluar dari aplikasi?"
    )

    if konfirmasi:
        root.destroy()


# =====================================
# 6. FRAME UTAMA
# =====================================

frame_utama = tk.Frame(
    root,
    bg=BG,
    width=660
)

frame_utama.grid(
    row=0,
    column=0,
    padx=15,
    pady=15
)

frame_utama.grid_columnconfigure(0, weight=1)


# =====================================
# 7. HEADER
# =====================================

header = tk.Frame(
    frame_utama,
    bg=NAVY,
    padx=25,
    pady=18
)

header.grid(
    row=0,
    column=0,
    sticky="ew"
)

tk.Label(
    header,
    text="UNIVERSITAS HASYIM ASY'ARI",
    font=("Arial", 12, "bold"),
    bg=NAVY,
    fg=WHITE
).grid(
    row=0,
    column=0,
    sticky="w"
)

tk.Label(
    header,
    text="FAKULTAS TEKNOLOGI INFORMASI",
    font=("Arial", 9),
    bg=NAVY,
    fg="#C8DCEB"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=4
)

tk.Label(
    header,
    text="FORMULIR IDENTITAS MAHASISWA",
    font=("Arial", 15, "bold"),
    bg=NAVY,
    fg=WHITE
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=(12, 3)
)

tk.Label(
    header,
    text="Silakan lengkapi data identitas mahasiswa dengan benar.",
    font=("Arial", 9),
    bg=NAVY,
    fg="#C8DCEB"
).grid(
    row=3,
    column=0,
    sticky="w"
)


# =====================================
# 8. FRAME FORMULIR
# =====================================

frame_form = tk.Frame(
    frame_utama,
    bg=WHITE,
    padx=25,
    pady=18
)

frame_form.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=12
)

frame_form.grid_columnconfigure(0, minsize=130)
frame_form.grid_columnconfigure(1, weight=1)

tk.Label(
    frame_form,
    text="DATA MAHASISWA",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(0, 12)
)


# =====================================
# 9. INPUT NAMA
# =====================================

tk.Label(
    frame_form,
    text="Nama Lengkap",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)

entry_nama = tk.Entry(
    frame_form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

entry_nama.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=(15, 0),
    ipady=5
)


# =====================================
# 10. INPUT NIM
# =====================================

tk.Label(
    frame_form,
    text="NIM",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=8
)

entry_nim = tk.Entry(
    frame_form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

entry_nim.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=(15, 0),
    ipady=5
)


# =====================================
# 11. JENIS KELAMIN
# =====================================

tk.Label(
    frame_form,
    text="Jenis Kelamin",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=3,
    column=0,
    sticky="w",
    pady=8
)

gender = tk.StringVar(value="")

frame_gender = tk.Frame(
    frame_form,
    bg=WHITE
)

frame_gender.grid(
    row=3,
    column=1,
    sticky="w",
    padx=10
)

tk.Radiobutton(
    frame_gender,
    text="Laki-laki",
    variable=gender,
    value="Laki-laki",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10),
    activebackground=WHITE
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Radiobutton(
    frame_gender,
    text="Perempuan",
    variable=gender,
    value="Perempuan",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10),
    activebackground=WHITE
).grid(
    row=0,
    column=1,
    padx=5
)


# =====================================
# 12. PROGRAM STUDI
# =====================================

tk.Label(
    frame_form,
    text="Program Studi",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=4,
    column=0,
    sticky="w",
    pady=8
)

combo_prodi = ttk.Combobox(
    frame_form,
    values=[
        "Teknik Informatika",
        "Sistem Informasi",
        "Teknologi Informasi"
    ],
    state="readonly",
    style="Custom.TCombobox"
)

combo_prodi.grid(
    row=4,
    column=1,
    sticky="ew",
    padx=(15, 0)
)


# =====================================
# 13. SEMESTER
# =====================================

tk.Label(
    frame_form,
    text="Semester",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=5,
    column=0,
    sticky="w",
    pady=8
)

combo_semester = ttk.Combobox(
    frame_form,
    values=[
        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6",
        "Semester 7",
        "Semester 8"
    ],
    state="readonly",
    style="Custom.TCombobox"
)

combo_semester.grid(
    row=5,
    column=1,
    sticky="ew",
    padx=(15, 0)
)


# =====================================
# 14. INPUT ALAMAT
# =====================================

tk.Label(
    frame_form,
    text="Alamat",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(
    row=6,
    column=0,
    sticky="nw",
    pady=10
)

text_alamat = tk.Text(
    frame_form,
    height=4,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    wrap="word"
)

text_alamat.grid(
    row=6,
    column=1,
    sticky="ew",
    padx=(15, 0),
    pady=5
)


# =====================================
# 15. FRAME TOMBOL
# =====================================

frame_tombol = tk.Frame(
    frame_utama,
    bg=BG
)

frame_tombol.grid(
    row=2,
    column=0,
    pady=5
)


# Tombol Simpan
tk.Button(
    frame_tombol,
    text="Simpan",
    command=simpan,
    bg=BLUE,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    width=14,
    relief="flat",
    cursor="hand2"
).grid(
    row=0,
    column=0,
    padx=6,
    ipady=6
)


# Tombol Reset
tk.Button(
    frame_tombol,
    text="Reset",
    command=reset,
    bg=GRAY,
    fg=WHITE,
    activebackground=TEXT,
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    width=14,
    relief="flat",
    cursor="hand2"
).grid(
    row=0,
    column=1,
    padx=6,
    ipady=6
)


# Tombol Keluar
tk.Button(
    frame_tombol,
    text="Keluar",
    command=keluar,
    bg=RED,
    fg=WHITE,
    activebackground="#922B21",
    activeforeground=WHITE,
    font=("Arial", 10, "bold"),
    width=14,
    relief="flat",
    cursor="hand2"
).grid(
    row=0,
    column=2,
    padx=6,
    ipady=6
)


# =====================================
# 16. FRAME HASIL IDENTITAS
# =====================================

frame_hasil = tk.Frame(
    frame_utama,
    bg=WHITE,
    padx=20,
    pady=15
)

frame_hasil.grid(
    row=3,
    column=0,
    sticky="ew",
    pady=10
)

frame_hasil.grid_columnconfigure(0, weight=1)

tk.Label(
    frame_hasil,
    text="HASIL IDENTITAS MAHASISWA",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=(0, 10)
)

# Label hasil input
hasil = tk.Label(
    frame_hasil,
    text="Data identitas akan ditampilkan di sini.",
    font=("Arial", 10),
    bg=LIGHT_BLUE,
    fg=GRAY,
    justify="left",
    anchor="nw",
    wraplength=550,
    padx=12,
    pady=12
)

hasil.grid(
    row=1,
    column=0,
    sticky="ew"
)


# =====================================
# 17. FOOTER
# =====================================

tk.Label(
    frame_utama,
    text="Sistem Formulir Identitas Mahasiswa | Praktikum Tkinter",
    font=("Arial", 8),
    bg=BG,
    fg=GRAY
).grid(
    row=4,
    column=0,
    pady=8
)


# =====================================
# 18. MENJALANKAN APLIKASI
# =====================================

entry_nama.focus()

root.mainloop()
