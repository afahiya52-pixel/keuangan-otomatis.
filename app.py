import streamlit as st
import re

# Set judul aplikasi web
st.set_page_config(page_title="Pencatat Keuangan Otomatis", page_icon="💰")
st.title("💰 Pencatat Keuangan Otomatis")
st.write("Ketik pengeluaranmu dengan kalimat biasa, sistem akan mendeteksinya!")

# Database sederhana (di memori session web)
if 'total_pengeluaran' not in st.session_state:
    st.session_state.total_pengeluaran = 0
    st.session_state.sisa_anggaran = 2000000  # Budget awal 2 juta
    st.session_state.riwayat = []

KATEGORI_MAP = {
    "Kebutuhan": ["bensin", "kos", "makan", "nasi", "buku", "sekolah"],
    "Jajan/Keinginan": ["kopi", "gandaria", "shopee", "bioskop", "boba", "seblak"],
    "Investasi": ["saham", "emas", "reksadana", "bibit", "jago"]
}

def catat_otomatis(teks):
    # Cari angka nominal uang
    angka_ditemukan = re.findall(r'\d+', teks)
    if not angka_ditemukan:
        st.error("❌ Nominal uang tidak ditemukan. Contoh: 'beli seblak 15000'")
        return

    nominal = int(angka_ditemukan[0])
    if "rb" in teks.lower() or "k" in teks.lower():
        if nominal < 1000:
            nominal *= 1000

    # Deteksi Kategori
    kategori_terdeteksi = "Lain-lain"
    teks_clean = teks.lower()
    for kategori, kata_kunci in KATEGORI_MAP.items():
        if any(kata in teks_clean for kata in kata_kunci):
            kategori_terdeteksi = kategori
            break

    # Update data budget
    st.session_state.total_pengeluaran += nominal
    st.session_state.sisa_anggaran -= nominal
    st.session_state.riwayat.append({
        "teks": teks,
        "nominal": nominal,
        "kategori": kategori_terdeteksi
    })
    st.success(f"✅ Berhasil dicatat: Rp {nominal:,} -> Kategori: {kategori_terdeteksi}")

# --- TAMPILAN INTERFACES WEB ---
# Input Teks dari User
input_user = st.text_input("Contoh: beli seblak 15rb atau nabung saham 100000", placeholder="Ketik di sini...")

if st.button("Catat Transaksi"):
    if input_user:
        catat_otomatis(input_user)
    else:
        st.warning("Isi kalimatnya dulu ya!")

st.markdown("---")

# Tampilan Status Anggaran
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Pengeluaran", f"Rp {st.session_state.total_pengeluaran:,}")
with col2:
    st.metric("Sisa Anggaran", f"Rp {st.session_state.sisa_anggaran:,}")

# Tampilkan Riwayat
if st.session_state.riwayat:
    st.subheader("📋 Riwayat Catatan:")
    for item in st.session_state.riwayat:
        st.write(f"- **{item['teks']}** (Rp {item['nominal']:,}) -> *[{item['kategori']}]*")
import streamlit as st

# --- 1. INISIALISASI ANGGARAN (Agar nilai tidak hilang saat diklik) ---
if "anggaran_total" not in st.session_state:
    st.session_state.anggaran_total = 2000000  # Nilai default awal (2 juta)

# --- 2. MEMBUAT SIDEBAR PERATURAN / PENGATURAN ---
# Semua kode di dalam blok "with st.sidebar:" akan otomatis muncul di sebelah kiri
with st.sidebar:
    st.title("⚙️ Peraturan Aplikasi")
    st.write("Silakan atur parameter keuanganmu di bawah ini:")
    
    # Kolom input untuk mengubah anggaran sesuka hati
    st.session_state.anggaran_total = st.number_input(
        "Set Total Anggaran (Rp):", 
        min_value=0, 
        value=st.session_state.anggaran_total, 
        step=50000
    )
    
    st.info("💡 Anggaran ini akan digunakan untuk menghitung sisa saldo di halaman utama.")

# --- 3. KODE HALAMAN UTAMA KAMU ---
st.title("Keuangan Otomatis")
# ... (lanjutkan dengan kode input teks "beli kopi 35" milikmu)
