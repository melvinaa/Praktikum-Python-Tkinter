
"""Aplikasi Penyimpanan Data Mahasiswa
Menggunakan Python, Tkinter, dan SQLite.
"""

import sqlite3
import tkinter as tk
from contextlib import contextmanager
from pathlib import Path
from tkinter import ttk, messagebox


# ==================================================
# 1. KONFIGURASI DATABASE
# ==================================================

DB_NAME = Path(__file__).resolve().parent / "mahasiswa.db"

DAFTAR_PRODI = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknologi Informasi"
]


@contextmanager
def koneksi():
    """Membuka koneksi, menyimpan perubahan, dan menutup koneksi."""
    conn = sqlite3.connect(DB_NAME)

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def buat_tabel():
    """Membuat tabel mahasiswa dan menambahkan kolom angkatan."""
    with koneksi() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                nim TEXT NOT NULL UNIQUE,
                prodi TEXT NOT NULL,
                alamat TEXT,
                angkatan INTEGER
            )
        """)

        # Memeriksa apakah kolom angkatan sudah tersedia
        kolom = conn.execute(
            "PRAGMA table_info(mahasiswa)"
        ).fetchall()

        nama_kolom = [item[1] for item in kolom]

        # Menambahkan kolom angkatan tanpa menghapus data lama
        if "angkatan" not in nama_kolom:
            conn.execute(
                "ALTER TABLE mahasiswa ADD COLUMN angkatan INTEGER"
            )


buat_tabel()


# ==================================================
# 2. MEMBUAT JENDELA UTAMA
# ==================================================

root = tk.Tk()
root.title("Aplikasi Data Mahasiswa")
root.geometry("1050x700")
root.minsize(850, 600)


# ==================================================
# 3. MEMBUAT FORMULIR MAHASISWA
# ==================================================

form = ttk.LabelFrame(
    root,
    text="Formulir Mahasiswa",
    padding=12
)
form.pack(fill="x", padx=15, pady=10)

# Input Nama
ttk.Label(form, text="Nama").grid(
    row=0, column=0, padx=5, pady=5, sticky="w"
)

entry_nama = ttk.Entry(form, width=30)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

# Input NIM
ttk.Label(form, text="NIM").grid(
    row=0, column=2, padx=5, pady=5, sticky="w"
)

entry_nim = ttk.Entry(form, width=30)
entry_nim.grid(row=0, column=3, padx=5, pady=5)

# Pilihan Program Studi
ttk.Label(form, text="Program Studi").grid(
    row=1, column=0, padx=5, pady=5, sticky="w"
)

combo_prodi = ttk.Combobox(
    form,
    values=DAFTAR_PRODI,
    state="readonly",
    width=27
)
combo_prodi.grid(row=1, column=1, padx=5, pady=5)

# Input Alamat
ttk.Label(form, text="Alamat").grid(
    row=1, column=2, padx=5, pady=5, sticky="w"
)

entry_alamat = ttk.Entry(form, width=30)
entry_alamat.grid(row=1, column=3, padx=5, pady=5)

# Input Angkatan
ttk.Label(form, text="Angkatan").grid(
    row=2, column=0, padx=5, pady=5, sticky="w"
)

entry_angkatan = ttk.Entry(form, width=30)
entry_angkatan.grid(row=2, column=1, padx=5, pady=5)


# ==================================================
# 4. MEMBUAT BAGIAN PENCARIAN
# ==================================================

frame_cari = ttk.LabelFrame(
    root,
    text="Pencarian Mahasiswa",
    padding=10
)
frame_cari.pack(fill="x", padx=15, pady=5)

ttk.Label(
    frame_cari,
    text="Masukkan Nama atau NIM:"
).pack(side="left", padx=5)

entry_cari = ttk.Entry(frame_cari, width=35)
entry_cari.pack(side="left", padx=5)


# ==================================================
# 5. MEMBUAT TABEL TREEVIEW
# ==================================================

kolom = (
    "id",
    "nama",
    "nim",
    "prodi",
    "alamat",
    "angkatan"
)

tabel = ttk.Treeview(
    root,
    columns=kolom,
    show="headings"
)

# Judul kolom
for key, judul in [
    ("id", "ID"),
    ("nama", "Nama"),
    ("nim", "NIM"),
    ("prodi", "Program Studi"),
    ("alamat", "Alamat"),
    ("angkatan", "Angkatan")
]:
    tabel.heading(key, text=judul)

# Mengatur lebar kolom
tabel.column("id", width=50, anchor="center")
tabel.column("nama", width=160)
tabel.column("nim", width=130)
tabel.column("prodi", width=170)
tabel.column("alamat", width=220)
tabel.column("angkatan", width=100, anchor="center")

tabel.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=8
)


# ==================================================
# 6. FUNGSI MENAMPILKAN DATA (SELECT)
# ==================================================

def tampilkan_data():
    """Mengambil dan menampilkan seluruh data mahasiswa."""

    for item in tabel.get_children():
        tabel.delete(item)

    with koneksi() as conn:
        rows = conn.execute("""
            SELECT id, nama, nim, prodi, alamat, angkatan
            FROM mahasiswa
            ORDER BY id ASC
        """).fetchall()

    for row in rows:
        tabel.insert("", tk.END, values=row)


# ==================================================
# 7. FUNGSI PENCARIAN MAHASISWA
# ==================================================

def cari_data():
    """Mencari mahasiswa berdasarkan nama atau NIM."""

    kata_kunci = entry_cari.get().strip()

    if not kata_kunci:
        tampilkan_data()
        return

    for item in tabel.get_children():
        tabel.delete(item)

    with koneksi() as conn:
        rows = conn.execute("""
            SELECT id, nama, nim, prodi, alamat, angkatan
            FROM mahasiswa
            WHERE nama LIKE ? OR nim LIKE ?
            ORDER BY id ASC
        """, (
            f"%{kata_kunci}%",
            f"%{kata_kunci}%"
        )).fetchall()

    for row in rows:
        tabel.insert("", tk.END, values=row)

    if not rows:
        messagebox.showinfo(
            "Pencarian",
            "Data mahasiswa tidak ditemukan."
        )


def tampilkan_semua():
    """Mengosongkan pencarian dan menampilkan seluruh data."""

    entry_cari.delete(0, tk.END)
    tampilkan_data()


# ==================================================
# 8. FUNGSI MEMBERSIHKAN FORMULIR
# ==================================================

def bersihkan_form():
    """Mengosongkan seluruh kolom formulir."""

    entry_nama.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    combo_prodi.set("")
    entry_alamat.delete(0, tk.END)
    entry_angkatan.delete(0, tk.END)

    entry_nama.focus_set()


# ==================================================
# 9. FUNGSI MENYIMPAN DATA (INSERT)
# ==================================================

def simpan_data():
    """Menyimpan data mahasiswa ke database."""

    nama = entry_nama.get().strip()
    nim = entry_nim.get().strip()
    prodi = combo_prodi.get().strip()
    alamat = entry_alamat.get().strip()
    angkatan_text = entry_angkatan.get().strip()

    # Validasi kolom wajib
    if not nama or not nim or not prodi or not angkatan_text:
        messagebox.showwarning(
            "Validasi",
            "Nama, NIM, Program Studi, dan Angkatan wajib diisi."
        )
        return

    # Validasi tipe data angkatan
    try:
        angkatan = int(angkatan_text)
    except ValueError:
        messagebox.showwarning(
            "Validasi",
            "Angkatan harus berupa angka."
        )
        return

    try:
        with koneksi() as conn:
            conn.execute("""
                INSERT INTO mahasiswa
                (nama, nim, prodi, alamat, angkatan)
                VALUES (?, ?, ?, ?, ?)
            """, (
                nama,
                nim,
                prodi,
                alamat,
                angkatan
            ))

        messagebox.showinfo(
            "Berhasil",
            "Data mahasiswa berhasil disimpan."
        )

        tampilkan_data()
        bersihkan_form()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "NIM Duplikat",
            "NIM sudah terdaftar."
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Kesalahan Database",
            str(error)
        )


# ==================================================
# 10. FUNGSI MENGAMBIL DATA TERPILIH
# ==================================================

def isi_form_dari_tabel(event=None):
    """Mengisi formulir berdasarkan baris yang dipilih."""
    
    pilihan = tabel.selection()

    if not pilihan:
        return

    record_id = int(
        tabel.item(pilihan[0], "values")[0]
    )

    with koneksi() as conn:
        row = conn.execute("""
            SELECT nama, nim, prodi, alamat, angkatan
            FROM mahasiswa
            WHERE id = ?
        """, (record_id,)).fetchone()

    if row is None:
        return

    bersihkan_form()

    entry_nama.insert(0, row[0])
    entry_nim.insert(0, row[1])
    combo_prodi.set(row[2])
    entry_alamat.insert(0, row[3] or "")

    if row[4] is not None:
        entry_angkatan.insert(0, str(row[4]))


# ==================================================
# 11. FUNGSI MENGUBAH DATA (UPDATE)
# ==================================================

def ubah_data():
    """Memperbarui data mahasiswa berdasarkan ID."""

    pilihan = tabel.selection()

    if not pilihan:
        messagebox.showwarning(
            "Pilih Data",
            "Pilih data mahasiswa yang akan diubah."
        )
        return

    record_id = int(
        tabel.item(pilihan[0], "values")[0]
    )

    nama = entry_nama.get().strip()
    nim = entry_nim.get().strip()
    prodi = combo_prodi.get().strip()
    alamat = entry_alamat.get().strip()
    angkatan_text = entry_angkatan.get().strip()

    if not nama or not nim or not prodi or not angkatan_text:
        messagebox.showwarning(
            "Validasi",
            "Nama, NIM, Program Studi, dan Angkatan wajib diisi."
        )
        return

    try:
        angkatan = int(angkatan_text)
    except ValueError:
        messagebox.showwarning(
            "Validasi",
            "Angkatan harus berupa angka."
        )
        return

    try:
        with koneksi() as conn:
            conn.execute("""
                UPDATE mahasiswa
                SET nama = ?,
                    nim = ?,
                    prodi = ?,
                    alamat = ?,
                    angkatan = ?
                WHERE id = ?
            """, (
                nama,
                nim,
                prodi,
                alamat,
                angkatan,
                record_id
            ))

        messagebox.showinfo(
            "Berhasil",
            "Data mahasiswa berhasil diperbarui."
        )

        tampilkan_data()
        bersihkan_form()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "NIM Duplikat",
            "NIM sudah digunakan mahasiswa lain."
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Kesalahan Database",
            str(error)
        )


# ==================================================
# 12. FUNGSI MENGHAPUS DATA (DELETE)
# ==================================================

def hapus_data():
    """Menghapus data mahasiswa yang dipilih."""

    pilihan = tabel.selection()

    if not pilihan:
        messagebox.showwarning(
            "Pilih Data",
            "Pilih data mahasiswa yang akan dihapus."
        )
        return

    data = tabel.item(pilihan[0], "values")
    record_id = int(data[0])

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        f"Apakah kamu yakin ingin menghapus data {data[1]}?"
    )

    if not konfirmasi:
        return

    try:
        with koneksi() as conn:
            conn.execute(
                "DELETE FROM mahasiswa WHERE id = ?",
                (record_id,)
            )

        messagebox.showinfo(
            "Berhasil",
            "Data mahasiswa berhasil dihapus."
        )

        tampilkan_data()
        bersihkan_form()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Kesalahan Database",
            str(error)
        )


# ==================================================
# 13. MENGHUBUNGKAN TREEVIEW DENGAN FORMULIR
# ==================================================

tabel.bind(
    "<<TreeviewSelect>>",
    isi_form_dari_tabel
)


# ==================================================
# 14. MEMBUAT TOMBOL PENCARIAN
# ==================================================

ttk.Button(
    frame_cari,
    text="Cari",
    command=cari_data
).pack(side="left", padx=5)

ttk.Button(
    frame_cari,
    text="Tampilkan Semua",
    command=tampilkan_semua
).pack(side="left", padx=5)


# ==================================================
# 15. MEMBUAT TOMBOL UTAMA
# ==================================================

baris_tombol = ttk.Frame(root)
baris_tombol.pack(fill="x", padx=15, pady=8)

ttk.Button(
    baris_tombol,
    text="Simpan Data",
    command=simpan_data
).pack(side="left", padx=4)

ttk.Button(
    baris_tombol,
    text="Ubah Data",
    command=ubah_data
).pack(side="left", padx=4)

ttk.Button(
    baris_tombol,
    text="Refresh",
    command=tampilkan_data
).pack(side="left", padx=4)

ttk.Button(
    baris_tombol,
    text="Bersihkan Form",
    command=bersihkan_form
).pack(side="left", padx=4)

ttk.Button(
    baris_tombol,
    text="Hapus Data Terpilih",
    command=hapus_data
).pack(side="right", padx=4)


# ==================================================
# 16. MENJALANKAN APLIKASI
# ==================================================

tampilkan_data()

root.mainloop()
