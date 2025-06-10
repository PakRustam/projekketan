import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Fungsi Keanggotaan
# -----------------------------

def fuzzy_harga(harga):
    rendah = max(min((15000 - harga) / 5000, 1), 0) if harga >= 10000 else 1
    sedang = max(min((harga - 15000) / 2500, 1), 0) if harga < 17500 else max(min((20000 - harga) / 2500, 1), 0)
    sedang = sedang if 15000 <= harga <= 20000 else 0
    mahal = max(min((harga - 20000) / 10000, 1), 0) if harga >= 20000 else 0
    return {'rendah': rendah, 'sedang': sedang, 'mahal': mahal}

def fuzzy_porsi(porsi):
    sedikit = max(min(2 - porsi, 1), 0) if porsi <= 2 else 0
    sedang = max(min(1 - abs(porsi - 2), 1), 0)
    banyak = max(min(porsi - 2, 1), 0) if porsi >= 2 else 0
    return {'sedikit': sedikit, 'sedang': sedang, 'banyak': banyak}

def fuzzy_jarak(jarak):
    dekat = max(min((1.5 - jarak) / 1.0, 1), 0) if jarak <= 1.5 else 0
    sedang = max(min(1 - abs(jarak - 2) / 1, 1), 0) if 1 <= jarak <= 3 else 0
    jauh = max(min((jarak - 2) / 2, 1), 0) if jarak >= 2 else 0
    return {'dekat': dekat, 'sedang': sedang, 'jauh': jauh}

# -----------------------------
# Inferensi Sugeno
# -----------------------------

def hitung_efisiensi(harga, porsi, jarak):
    fuzzy_h = fuzzy_harga(harga)
    fuzzy_p = fuzzy_porsi(porsi)
    fuzzy_j = fuzzy_jarak(jarak)

    # Perhitungan efisiensi berdasarkan bobot aturan
    rules = []
    def add_rule(h, p, j, output):
        w = fuzzy_h[h] * fuzzy_p[p] * fuzzy_j[j]
        rules.append((w, output))

    # Aturan-aturan fuzzy
    add_rule('rendah', 'banyak', 'dekat', 95)
    add_rule('rendah', 'sedang', 'sedang', 85)
    add_rule('sedang', 'banyak', 'sedang', 80)
    add_rule('mahal', 'banyak', 'dekat', 75)
    add_rule('mahal', 'sedikit', 'jauh', 30)
    add_rule('rendah', 'sedikit', 'jauh', 40)
    add_rule('sedang', 'sedikit', 'jauh', 60)
    add_rule('sedang', 'sedang', 'sedang', 70)
    add_rule('rendah', 'banyak', 'jauh', 80)

    numerator = sum(w * z for w, z in rules)
    denominator = sum(w for w, _ in rules)

    return numerator / denominator if denominator != 0 else 0

# -----------------------------
# Data Tempat Makan
# -----------------------------

tempat_makan = [
    {"nama": "Bu Adib", "harga": 11000, "porsi": 1.5, "jarak": 0.5},
    {"nama": "Mbahkakung", "harga": 15000, "porsi": 2.0, "jarak": 1.2},
    {"nama": "Gacoan", "harga": 11000, "porsi": 1.0, "jarak": 1.5},
    {"nama": "Pak Rustam", "harga": 13000, "porsi": 1.0, "jarak": 2.2},
    {"nama": "Ekarasa", "harga": 10000, "porsi": 1.5, "jarak": 2.0},
    {"nama": "Bebek Bumbu", "harga": 17000, "porsi": 2.5, "jarak": 2.5},
    {"nama": "Warteg Barokah", "harga": 8000, "porsi": 1.0, "jarak": 0.7},
    {"nama": "Sate H. Darto", "harga": 21000, "porsi": 2.8, "jarak": 3.0},
    {"nama": "Warung Makan Bu Tini", "harga": 12000, "porsi": 2.0, "jarak": 0.3},
    {"nama": "Kedai 99 FMIPA", "harga": 15000, "porsi": 2.2, "jarak": 0.1},
    {"nama": "Nasi Goreng Matematika", "harga": 13000, "porsi": 1.8, "jarak": 0.4},
    {"nama": "Ayam Geprek Kimia", "harga": 16000, "porsi": 2.0, "jarak": 0.6},
    {"nama": "Bakso Fisika", "harga": 10000, "porsi": 1.5, "jarak": 0.2},
    {"nama": "Mie Ayam Biologi", "harga": 12000, "porsi": 1.7, "jarak": 0.5},
    {"nama": "Soto Informatika", "harga": 14000, "porsi": 2.0, "jarak": 0.7},
    {"nama": "Es Teh Statistika", "harga": 5000, "porsi": 1.0, "jarak": 0.3},
    {"nama": "Warung Kopi Dosen", "harga": 8000, "porsi": 1.2, "jarak": 0.4},
    {"nama": "Kantin FMIPA", "harga": 10000, "porsi": 1.5, "jarak": 0.0},
    {"nama": "Nasi Padang FMIPA", "harga": 18000, "porsi": 2.3, "jarak": 0.2},
    {"nama": "Sego Macan", "harga": 15000, "porsi": 2.5, "jarak": 1.0},
    {"nama": "Warung Steak FMIPA", "harga": 20000, "porsi": 2.0, "jarak": 0.8},
    {"nama": "Bebek Goreng FMIPA", "harga": 17000, "porsi": 2.2, "jarak": 0.5},
    {"nama": "Mie Ayam FMIPA", "harga": 12000, "porsi": 1.8, "jarak": 0.3},
    {"nama": "Sate FMIPA", "harga": 15000, "porsi": 1.5, "jarak": 0.4},
    {"nama": "Bakso Malang FMIPA", "harga": 13000, "porsi": 1.7, "jarak": 0.6},
]

# -----------------------------
# Konfigurasi Streamlit
# -----------------------------

st.set_page_config(page_title="Sistem Rekomendasi Tempat Makan", page_icon="🍽️", layout="wide")

# Header aplikasi
st.title("🍽️ Sistem Rekomendasi Tempat Makan Fuzzy Logic")
st.markdown("""
**Aplikasi ini membantu Anda menemukan tempat makan terbaik berdasarkan:**
- Budget yang Anda miliki
- Preferensi jarak tempat makan
- Preferensi porsi makanan
""")
st.divider()

# -----------------------------
# Input dari Pengguna
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Budget Anda")
    budget = st.slider("Pilih budget (Rp)", 5000, 30000, 15000, 1000, format="Rp%d")

with col2:
    st.subheader("Preferensi Jarak")
    preferensi_jarak = st.selectbox("Pilih preferensi jarak", 
                                  ["dekat", "sedang", "jauh"],
                                  index=0)

with col3:
    st.subheader("Preferensi Porsi")
    preferensi_porsi = st.selectbox("Pilih preferensi porsi", 
                                  ["sedikit", "sedang", "banyak"],
                                  index=1)

# -----------------------------
# Filtering Berdasarkan Preferensi Jarak
# -----------------------------

if preferensi_jarak == 'dekat':
    filtered_tempat = [t for t in tempat_makan if t['jarak'] <= 1.5]
elif preferensi_jarak == 'sedang':
    filtered_tempat = [t for t in tempat_makan if 1.5 < t['jarak'] <= 3.0]
else:  # jauh
    filtered_tempat = [t for t in tempat_makan if t['jarak'] > 3.0]

# -----------------------------
# Hitung Efisiensi
# -----------------------------

for tempat in filtered_tempat:
    # Konversi preferensi porsi ke nilai numerik
    porsi_numerik = 1 if preferensi_porsi == 'sedikit' else 2 if preferensi_porsi == 'sedang' else 2.8
    
    efisiensi = hitung_efisiensi(
        tempat['harga'],
        porsi_numerik,
        tempat['jarak']
    )
    tempat['efisiensi'] = efisiensi

# Filter berdasarkan budget dan urutkan
final_tempat = [t for t in filtered_tempat if t['harga'] <= budget]
final_tempat.sort(key=lambda x: (-x['efisiensi'], x['harga']))

# -----------------------------
# Output Rekomendasi
# -----------------------------

st.divider()
st.subheader("🔥 Rekomendasi Tempat Makan Paling Efisien")

if not final_tempat:
    st.warning("Tidak ada tempat makan yang sesuai dengan preferensi Anda.")
else:
    # Tampilkan tempat terbaik di bagian atas
    best = final_tempat[0]
    st.success(f"**REKOMENDASI TERBAIK: {best['nama']}**")
    
    # Tampilkan peta perbandingan
    cols = st.columns([1, 3])
    with cols[0]:
        st.metric("Efisiensi", f"{best['efisiensi']:.2f}")
        st.metric("Harga", f"Rp{best['harga']:,.0f}")
        st.metric("Jarak", f"{best['jarak']} km")
        st.metric("Porsi", best['porsi'])
    
    with cols[1]:
        # Grafik perbandingan rekomendasi teratas
        top5 = final_tempat[:min(5, len(final_tempat))]
        names = [t['nama'] for t in top5]
        efficiencies = [t['efisiensi'] for t in top5]
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bars = ax.barh(names, efficiencies, color='#FF6B6B')
        ax.set_xlim(0, 100)
        ax.set_xlabel('Skor Efisiensi')
        ax.set_title('Perbandingan Rekomendasi Teratas')
        ax.bar_label(bars, fmt='%.2f', padding=3)
        st.pyplot(fig)
    
    # Tampilkan semua rekomendasi dalam tabel
    st.subheader("Semua Rekomendasi")
    for i, tempat in enumerate(final_tempat[:10], 1):
        st.markdown(f"""
        ##### {i}. {tempat['nama']}
        - **Harga:** Rp{tempat['harga']:,.0f} | **Porsi:** {tempat['porsi']} | **Jarak:** {tempat['jarak']} km
        - **Skor Efisiensi:** `{tempat['efisiensi']:.2f}`
        """)
        st.progress(tempat['efisiensi'] / 100)

# -----------------------------
# Grafik Fungsi Keanggotaan
# -----------------------------

st.divider()
st.subheader("📊 Fungsi Keanggotaan Fuzzy Logic")

def plot_fuzzy_membership():
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    
    # Grafik Harga
    x_harga = np.linspace(5000, 30000, 100)
    y_rendah = [fuzzy_harga(x)['rendah'] for x in x_harga]
    y_sedang = [fuzzy_harga(x)['sedang'] for x in x_harga]
    y_mahal = [fuzzy_harga(x)['mahal'] for x in x_harga]
    
    axs[0].plot(x_harga, y_rendah, label='Rendah', linewidth=2)
    axs[0].plot(x_harga, y_sedang, label='Sedang', linewidth=2)
    axs[0].plot(x_harga, y_mahal, label='Mahal', linewidth=2)
    axs[0].set_title('Fungsi Keanggotaan Harga')
    axs[0].set_xlabel('Harga (Rp)')
    axs[0].set_ylabel('Derajat Keanggotaan')
    axs[0].legend()
    axs[0].grid(True, linestyle='--', alpha=0.7)
    
    # Garis untuk budget user
    axs[0].axvline(x=budget, color='r', linestyle='--', alpha=0.7)
    axs[0].text(budget+500, 0.9, f'Budget Anda: Rp{budget:,.0f}', rotation=0)

    # Grafik Porsi
    x_porsi = np.linspace(0.5, 3.5, 100)
    y_sedikit = [fuzzy_porsi(x)['sedikit'] for x in x_porsi]
    y_sedang_porsi = [fuzzy_porsi(x)['sedang'] for x in x_porsi]
    y_banyak = [fuzzy_porsi(x)['banyak'] for x in x_porsi]
    
    axs[1].plot(x_porsi, y_sedikit, label='Sedikit', linewidth=2)
    axs[1].plot(x_porsi, y_sedang_porsi, label='Sedang', linewidth=2)
    axs[1].plot(x_porsi, y_banyak, label='Banyak', linewidth=2)
    axs[1].set_title('Fungsi Keanggotaan Porsi')
    axs[1].set_xlabel('Porsi')
    axs[1].set_ylabel('Derajat Keanggotaan')
    axs[1].legend()
    axs[1].grid(True, linestyle='--', alpha=0.7)
    
    # Garis untuk preferensi porsi user
    porsi_val = 1 if preferensi_porsi == 'sedikit' else 2 if preferensi_porsi == 'sedang' else 2.8
    axs[1].axvline(x=porsi_val, color='r', linestyle='--', alpha=0.7)
    axs[1].text(porsi_val+0.05, 0.9, f'Preferensi Anda: {preferensi_porsi}', rotation=0)

    # Grafik Jarak
    x_jarak = np.linspace(0, 5, 100)
    y_dekat = [fuzzy_jarak(x)['dekat'] for x in x_jarak]
    y_sedang_jarak = [fuzzy_jarak(x)['sedang'] for x in x_jarak]
    y_jauh = [fuzzy_jarak(x)['jauh'] for x in x_jarak]
    
    axs[2].plot(x_jarak, y_dekat, label='Dekat', linewidth=2)
    axs[2].plot(x_jarak, y_sedang_jarak, label='Sedang', linewidth=2)
    axs[2].plot(x_jarak, y_jauh, label='Jauh', linewidth=2)
    axs[2].set_title('Fungsi Keanggotaan Jarak')
    axs[2].set_xlabel('Jarak (km)')
    axs[2].set_ylabel('Derajat Keanggotaan')
    axs[2].legend()
    axs[2].grid(True, linestyle='--', alpha=0.7)
    
    # Garis untuk preferensi jarak user
    jarak_val = 0.5 if preferensi_jarak == 'dekat' else 2.0 if preferensi_jarak == 'sedang' else 3.5
    axs[2].axvline(x=jarak_val, color='r', linestyle='--', alpha=0.7)
    axs[2].text(jarak_val+0.1, 0.9, f'Preferensi Anda: {preferensi_jarak}', rotation=0)

    plt.tight_layout()
    return fig

st.pyplot(plot_fuzzy_membership())

# -----------------------------
# Footer
# -----------------------------

st.divider()
st.caption("""
**Penjelasan Sistem:**
- **Harga:** Rendah (< Rp15.000), Sedang (Rp15.000-20.000), Mahal (> Rp20.000)
- **Porsi:** Sedikit (<2), Sedang (2), Banyak (>2)
- **Jarak:** Dekat (<1.5 km), Sedang (1.5-3 km), Jauh (>3 km)
- **Skor Efisiensi:** Diukur dari 0-100 (semakin tinggi semakin baik)
""")