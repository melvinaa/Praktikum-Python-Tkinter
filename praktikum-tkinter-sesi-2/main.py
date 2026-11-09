import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Pendaftaran Kegiatan Mahasiswa")
root.geometry("900x800")
root.configure(bg="#EAF2F8")

# Variabel
nama = tk.StringVar()
prodi = tk.StringVar()
gender = tk.StringVar()

kegiatan = [
    "Olimpiade Mahasiswa",
    "Program Kreativitas Mahasiswa (PKM)",
    "Lomba Karya Tulis Ilmiah (LKTI)",
    "Seminar Nasional",
    "Seminar Internasional",
    "Workshop dan Pelatihan",
    "Kompetisi Debat",
    "Lomba Esai",
    "Hackathon",
    "Kompetisi Pemrograman",
    "Badan Eksekutif Mahasiswa (BEM)",
    "Himpunan Mahasiswa Program Studi (HMPS)",
    "Dewan Perwakilan Mahasiswa (DPM)",
    "Unit Kegiatan Mahasiswa (UKM)",
    "Pelatihan Kepemimpinan Mahasiswa",
    "Latihan Dasar Kepemimpinan (LDK)",
    "Bakti Sosial",
    "Pengabdian kepada Masyarakat",
    "Relawan Mahasiswa",
    "Donor Darah",
    "Kampanye Lingkungan",
    "Kuliah Kerja Nyata (KKN)",
    "Futsal", "Badminton", "Basket", "Voli", "Sepak Bola",
    "E-Sports", "Pencak Silat",
    "Festival Seni dan Budaya", "Paduan Suara", "Tari Tradisional",
    "Musik dan Band", "Fotografi", "Desain Grafis", "Teater",
    "Program Wirausaha Mahasiswa", "Kompetisi Business Plan",
    "Pelatihan Digital Marketing", "Job Fair dan Career Development",
    "Magang Mahasiswa", "Pelatihan Public Speaking"
]
pilihan = [tk.BooleanVar() for _ in kegiatan]


def about():
    jendela = tk.Toplevel(root)
    jendela.title("About")
    jendela.geometry("350x170")
    tk.Label(jendela, text="Pendaftaran Kegiatan Mahasiswa",
             font=("Arial", 13, "bold")).pack(pady=20)
    tk.Label(jendela, text="Aplikasi Python Tkinter\nPraktikum Sesi 11").pack(pady=5)
    ttk.Button(jendela, text="Tutup", command=jendela.destroy).pack(pady=10)


def update_listbox():
    listbox.delete(0, tk.END)
    for i, item in enumerate(kegiatan):
        if pilihan[i].get():
            listbox.insert(tk.END, item)


def submit():
    if not nama.get().strip():
        messagebox.showwarning("Peringatan", "Nama tidak boleh kosong!")
        entry_nama.focus()
        return
    if not prodi.get() or not gender.get():
        messagebox.showwarning("Peringatan", "Pilih program studi dan jenis kelamin!")
        return

    dipilih = [kegiatan[i] for i in range(len(kegiatan)) if pilihan[i].get()]
    if not dipilih:
        messagebox.showwarning("Peringatan", "Pilih minimal satu kegiatan!")
        return

    alasan = text_alasan.get("1.0", tk.END).strip() or "-"
    hasil = (
        "RINGKASAN PENDAFTARAN\n"
        "------------------------------\n"
        f"Nama: {nama.get()}\n"
        f"Program Studi: {prodi.get()}\n"
        f"Jenis Kelamin: {gender.get()}\n\n"
        "Kegiatan:\n" + "\n".join("- " + x for x in dipilih) +
        f"\n\nAlasan: {alasan}"
    )

    hasil_text.config(state="normal")
    hasil_text.delete("1.0", tk.END)
    hasil_text.insert(tk.END, hasil)
    hasil_text.config(state="disabled")
    messagebox.showinfo("Berhasil", "Pendaftaran berhasil disimpan!")


def reset():
    nama.set("")
    prodi.set("")
    gender.set("")
    for item in pilihan:
        item.set(False)
    text_alasan.delete("1.0", tk.END)
    update_listbox()
    hasil_text.config(state="normal")
    hasil_text.delete("1.0", tk.END)
    hasil_text.config(state="disabled")


# Menu
menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Keluar", command=root.destroy)
menu.add_cascade(label="File", menu=file_menu)
help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="About", command=about)
menu.add_cascade(label="Bantuan", menu=help_menu)
root.config(menu=menu)

# Judul
tk.Label(root, text="FORMULIR PENDAFTARAN KEGIATAN MAHASISWA",
         font=("Arial", 15, "bold"), bg="#EAF2F8",
         fg="#1F4E79").pack(pady=10)

# Data mahasiswa
data_frame = tk.LabelFrame(root, text="Data Mahasiswa", bg="#EAF2F8", padx=10, pady=8)
data_frame.pack(fill="x", padx=15, pady=5)

tk.Label(data_frame, text="Nama Lengkap", bg="#EAF2F8").grid(row=0, column=0, sticky="w", pady=5)
entry_nama = ttk.Entry(data_frame, textvariable=nama, width=45)
entry_nama.grid(row=0, column=1, sticky="w", padx=8)

tk.Label(data_frame, text="Program Studi", bg="#EAF2F8").grid(row=1, column=0, sticky="w", pady=5)
ttk.Combobox(data_frame, textvariable=prodi,
             values=["Sistem Informasi", "Teknologi Informasi", "Teknik Informatika"],
             state="readonly", width=42).grid(row=1, column=1, sticky="w", padx=8)

tk.Label(data_frame, text="Jenis Kelamin", bg="#EAF2F8").grid(row=2, column=0, sticky="w", pady=5)
gender_frame = tk.Frame(data_frame, bg="#EAF2F8")
gender_frame.grid(row=2, column=1, sticky="w")
tk.Radiobutton(gender_frame, text="Laki-laki", variable=gender,
               value="Laki-laki", bg="#EAF2F8").pack(side="left")
tk.Radiobutton(gender_frame, text="Perempuan", variable=gender,
               value="Perempuan", bg="#EAF2F8").pack(side="left", padx=10)

# Pilihan Checkbutton dengan scrollbar
kegiatan_frame = tk.LabelFrame(root, text="Pilih Kegiatan (boleh lebih dari satu)",
                               bg="#EAF2F8", padx=8, pady=5)
kegiatan_frame.pack(fill="both", expand=True, padx=15, pady=5)

canvas = tk.Canvas(kegiatan_frame, height=145, bg="#EAF2F8", highlightthickness=0)
scroll = ttk.Scrollbar(kegiatan_frame, orient="vertical", command=canvas.yview)
isi_kegiatan = tk.Frame(canvas, bg="#EAF2F8")
isi_kegiatan.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=isi_kegiatan, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

for i, item in enumerate(kegiatan):
    tk.Checkbutton(isi_kegiatan, text=item, variable=pilihan[i],
                   command=update_listbox, bg="#EAF2F8",
                   anchor="w").grid(row=i // 2, column=i % 2, sticky="w", padx=8)

# Listbox
list_frame = tk.LabelFrame(root, text="Kegiatan yang Dipilih", bg="#EAF2F8", padx=8, pady=5)
list_frame.pack(fill="x", padx=15, pady=5)
listbox = tk.Listbox(list_frame, height=3)
listbox.pack(fill="x")

# Alasan
alasan_frame = tk.LabelFrame(root, text="Alasan Mengikuti Kegiatan", bg="#EAF2F8", padx=8, pady=5)
alasan_frame.pack(fill="x", padx=15, pady=5)
text_alasan = tk.Text(alasan_frame, height=2)
text_alasan.pack(fill="x")

# Tombol
tombol_frame = tk.Frame(root, bg="#EAF2F8")
tombol_frame.pack(pady=7)
ttk.Button(tombol_frame, text="Submit", command=submit).pack(side="left", padx=8)
ttk.Button(tombol_frame, text="Reset", command=reset).pack(side="left", padx=8)

# Ringkasan
hasil_frame = tk.LabelFrame(root, text="Informasi Pendaftaran", bg="#EAF2F8", padx=8, pady=5)
hasil_frame.pack(fill="both", expand=True, padx=15, pady=5)
hasil_text = tk.Text(hasil_frame, height=5, state="disabled", wrap="word")
hasil_text.pack(fill="both", expand=True)

root.bind("<Return>", lambda event: submit())
entry_nama.focus()
root.mainloop()
