import os
import sys
import subprocess
import time
import math

# --- DOSYA İÇERİĞİ (V25 - YEŞİL KUTU KALDIRILDI & SAYI SINIRI DÜZELTİLDİ) ---
dosya_icerigi = """
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import math

# --- HARİTA KÜTÜPHANELERİ ---
try:
    import folium
    from streamlit_folium import st_folium
except ImportError:
    st.error("Lütfen harita kütüphanesini yükleyin: `pip install folium streamlit-folium`")
    st.stop()

# Sayfa Ayarları
st.set_page_config(page_title="Lojistik Platformu", layout="wide")

# --- KOORDİNAT VERİTABANI (GENİŞLETİLMİŞ AVRUPA) ---
SEHIR_KOORDINATLARI = {
    # TÜRKİYE
    "Adana": [37.0000, 35.3213], "Adıyaman": [37.7648, 38.2786], "Afyonkarahisar": [38.7507, 30.5567],
    "Ağrı": [39.7191, 43.0503], "Aksaray": [38.3687, 34.0370], "Amasya": [40.6499, 35.8353],
    "Ankara": [39.9334, 32.8597], "Antalya": [36.8841, 30.7056], "Ardahan": [41.1105, 42.7022],
    "Artvin": [41.1828, 41.8183], "Aydın": [37.8444, 27.8458], "Balıkesir": [39.6484, 27.8826],
    "Bartın": [41.6344, 32.3375], "Batman": [37.8812, 41.1351], "Bayburt": [40.2552, 40.2249],
    "Bilecik": [40.1451, 29.9798], "Bingöl": [38.8853, 40.4980], "Bitlis": [38.3938, 42.1232],
    "Bolu": [40.7350, 31.6061], "Burdur": [37.7204, 30.2908], "Bursa": [40.1885, 29.0610],
    "Çanakkale": [40.1553, 26.4142], "Çankırı": [40.6013, 33.6134], "Çorum": [40.5506, 34.9556],
    "Denizli": [37.7765, 29.0864], "Diyarbakır": [37.9144, 40.2306], "Düzce": [40.8438, 31.1565],
    "Edirne": [41.6768, 26.5603], "Elazığ": [38.6810, 39.2264], "Erzincan": [39.7500, 39.5000],
    "Erzurum": [39.9043, 41.2679], "Eskişehir": [39.7667, 30.5256], "Gaziantep": [37.0662, 37.3833],
    "Giresun": [40.9128, 38.3895], "Gümüşhane": [40.4600, 39.4700], "Hakkari": [37.5833, 43.7333],
    "Hatay": [36.4018, 36.3498], "Iğdır": [39.9167, 44.0333], "Isparta": [37.7648, 30.5566],
    "İstanbul": [41.0082, 28.9784], "İzmir": [38.4192, 27.1287], "Kahramanmaraş": [37.5858, 36.9371],
    "Karabük": [41.2061, 32.6204], "Karaman": [37.1759, 33.2287], "Kars": [40.6172, 43.0974],
    "Kastamonu": [41.3887, 33.7827], "Kayseri": [38.7312, 35.4787], "Kilis": [36.7184, 37.1212],
    "Kırıkkale": [39.8468, 33.5153], "Kırklareli": [41.7333, 27.2167], "Kırşehir": [39.1425, 34.1709],
    "Kocaeli": [40.8533, 29.8815], "Konya": [37.8667, 32.4833], "Kütahya": [39.4167, 29.9833],
    "Malatya": [38.3552, 38.3095], "Manisa": [38.6191, 27.4289], "Mardin": [37.3212, 40.7245],
    "Mersin": [36.8000, 34.6333], "Muğla": [37.2153, 28.3636], "Muş": [38.9462, 41.7539],
    "Nevşehir": [38.6939, 34.6857], "Niğde": [37.9667, 34.6833], "Ordu": [40.9839, 37.8764],
    "Osmaniye": [37.0742, 36.2476], "Rize": [41.0201, 40.5234], "Sakarya": [40.7569, 30.3783],
    "Samsun": [41.2867, 36.33], "Şanlıurfa": [37.1591, 38.7969], "Siirt": [37.9333, 41.9500],
    "Sinop": [42.0231, 35.1531], "Sivas": [39.7477, 37.0179], "Şırnak": [37.5164, 42.4611],
    "Tekirdağ": [40.9833, 27.5167], "Tokat": [40.3167, 36.5500], "Trabzon": [41.0015, 39.7178],
    "Tunceli": [39.1079, 39.5401], "Uşak": [38.6823, 29.4082], "Van": [38.4891, 43.4089],
    "Yalova": [40.6500, 29.2667], "Yozgat": [39.8181, 34.8147], "Zonguldak": [41.4564, 31.7987],
    
    # BATI AVRUPA
    "Almanya": [52.5200, 13.4050], "Fransa": [48.8566, 2.3522], "Hollanda": [52.3676, 4.9041],
    "Belçika": [50.8503, 4.3517], "Lüksemburg": [49.8153, 6.1296], "İngiltere": [51.5074, -0.1278],
    "İrlanda": [53.3498, -6.2603],
    
    # GÜNEY AVRUPA
    "İtalya": [41.9028, 12.4964], "İspanya": [40.4168, -3.7038], "Portekiz": [38.7223, -9.1393],
    "Yunanistan": [37.9838, 23.7275], "Malta": [35.9375, 14.3754], "Kıbrıs": [35.1856, 33.3823],
    "Andorra": [42.5063, 1.5218], "San Marino": [43.9424, 12.4578], "Monako": [43.7384, 7.4246],
    
    # ORTA AVRUPA
    "Avusturya": [48.2082, 16.3738], "İsviçre": [46.9480, 7.4474], "Polonya": [52.2297, 21.0122],
    "Macaristan": [47.4979, 19.0402], "Çekya": [50.0755, 14.4378], "Slovakya": [48.1486, 17.1077],
    "Slovenya": [46.0569, 14.5058], "Lihtenştayn": [47.1410, 9.5209],
    
    # KUZEY AVRUPA
    "İsveç": [59.3293, 18.0686], "Norveç": [59.9139, 10.7522], "Danimarka": [55.6761, 12.5683],
    "Finlandiya": [60.1699, 24.9384], "İzlanda": [64.1466, -21.9426],
    "Estonya": [59.4370, 24.7536], "Letonya": [56.9496, 24.1052], "Litvanya": [54.6872, 25.2797],
    
    # DOĞU AVRUPA & BALKANLAR
    "Bulgaristan": [42.6977, 23.3219], "Romanya": [44.4268, 26.1025],
    "Hırvatistan": [45.8150, 15.9819], "Sırbistan": [44.7866, 20.4489], 
    "Bosna-Hersek": [43.8563, 18.4131], "Karadağ": [42.4304, 19.2594],
    "Kuzey Makedonya": [41.9981, 21.4254], "Arnavutluk": [41.3275, 19.8187],
    "Kosova": [42.6629, 21.1655], "Ukrayna": [50.4501, 30.5234], 
    "Moldova": [47.0105, 28.8638], "Beyaz Rusya": [53.9045, 27.5615]
}

# --- CSS ---
st.markdown(\"\"\"
    <style>
    .stButton>button {
        background-color: #d90429 !important;
        color: white !important;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        padding: 8px 20px;
        font-size: 14px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #b00322 !important;
        transform: scale(1.02);
    }
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
        color: #d90429 !important;
    }
    .stExpander {
        border: 1px solid #d90429;
        border-radius: 5px;
    }
    </style>
\"\"\", unsafe_allow_html=True)

# --- VERİTABANI ---
if 'ilanlar' not in st.session_state:
    st.session_state.ilanlar = pd.DataFrame(columns=[
        "ID", "Tarih", "Nakliyeci", "Telefon", "Kapsam", "Yük_Tipi", "Nereden", "Nereye", 
        "Yük_Miktarı_Ton", "Satis_Fiyati", "Ücret", "Para_Birimi", "Süre_Saat", "Notlar", "Durum"
    ])

if 'basvurular' not in st.session_state:
    st.session_state.basvurular = {}

if 'giris_yapildi' not in st.session_state:
    st.session_state['giris_yapildi'] = False
if 'aktif_rol' not in st.session_state:
    st.session_state['aktif_rol'] = ""
if 'login_error' not in st.session_state:
    st.session_state['login_error'] = False

turkiye_illeri = sorted([k for k in SEHIR_KOORDINATLARI.keys() if k in ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]])

avrupa_ulkeleri = sorted([k for k in SEHIR_KOORDINATLARI.keys() if k not in turkiye_illeri])

# --- YARDIMCI FONKSİYONLAR ---
def mesafe_hesapla(konum1, konum2):
    lat1, lon1 = map(math.radians, konum1)
    lat2, lon2 = map(math.radians, konum2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # km
    return c * r

# --- CALLBACK FONKSİYONLARI ---
def cb_giris_yap():
    rol = st.session_state.get("inp_rol")
    pw = st.session_state.get("inp_pass")
    if rol and rol != "Seçiniz...":
        if pw == "1234":
            st.session_state['giris_yapildi'] = True
            st.session_state['aktif_rol'] = rol
            st.session_state['login_error'] = False
        else: st.session_state['login_error'] = True
    else: st.session_state['login_error'] = False

def cb_cikis_yap():
    st.session_state['giris_yapildi'] = False
    st.session_state['aktif_rol'] = ""

def cb_ilan_yayinla():
    ad = st.session_state.get("n_ad")
    tel = st.session_state.get("n_tel")
    kapsam = st.session_state.get("n_kapsam")
    nereden = st.session_state.get("n_nereden")
    nereye = st.session_state.get("n_nereye")
    yuk_tipi = st.session_state.get("n_yuk")
    tonaj = st.session_state.get("n_ton")
    satis = st.session_state.get("n_satis")
    ucret = st.session_state.get("n_ucret")
    birim = st.session_state.get("n_birim")
    sure = st.session_state.get("n_sure")
    notlar = st.session_state.get("n_not")

    if not (ad and tel and yuk_tipi and nereden != "Seçiniz..." and nereye != "Seçiniz..."):
        st.session_state['form_msg'] = ("error", "Eksik Bilgi Girdiniz!")
    elif nereden == nereye:
        st.session_state['form_msg'] = ("error", "Giriş ve Çıkış aynı olamaz!")
    else:
        yeni_veri = {
            "ID": len(st.session_state.ilanlar) + 1,
            "Tarih": datetime.now().strftime("%Y-%m-%d"),
            "Nakliyeci": ad, "Telefon": tel, "Kapsam": kapsam,
            "Yük_Tipi": yuk_tipi,
            "Nereden": nereden, "Nereye": nereye, "Yük_Miktarı_Ton": tonaj,
            "Satis_Fiyati": satis, "Ücret": ucret, "Para_Birimi": birim,
            "Süre_Saat": sure, "Notlar": notlar, "Durum": "Aktif"
        }
        st.session_state.ilanlar = pd.concat([st.session_state.ilanlar, pd.DataFrame([yeni_veri])], ignore_index=True)
        st.session_state['form_msg'] = ("success", "✅ İlan yayınlandı")

def cb_basvuru_yap(id_val):
    ehliyet = st.session_state.get(f"ehliyet_{id_val}")
    foto = st.session_state.get(f"foto_{id_val}")
    if ehliyet and foto:
        st.session_state.basvurular[id_val] = {"status": "Bekliyor", "ehliyet": ehliyet.getvalue(), "foto": foto.getvalue()}

def cb_isi_kabul_et(id_val):
    idx = st.session_state.ilanlar[st.session_state.ilanlar["ID"] == id_val].index[0]
    st.session_state.ilanlar.at[idx, "Durum"] = "Alındı"

def cb_teslim_et(row_index):
    st.session_state.ilanlar.at[row_index, "Durum"] = "Tamamlandı"

def cb_yonetici_onay(pid):
    st.session_state.basvurular[pid]["status"] = "Onaylandi"

def cb_yonetici_red(pid):
    st.session_state.basvurular[pid]["status"] = "Reddedildi"

def cb_sistemi_sifirla():
    st.session_state.ilanlar = st.session_state.ilanlar[0:0]
    st.session_state.basvurular = {}

# --- ARAYÜZ ---
st.sidebar.title("🔐 Güvenli Giriş")

if not st.session_state['giris_yapildi']:
    st.sidebar.selectbox("Giriş Türü:", ["Seçiniz...", "Nakliyeci Girişi", "Şoför Girişi", "Yönetici Girişi"], key="inp_rol")
    st.sidebar.text_input("Şifre:", type="password", key="inp_pass")
    st.sidebar.button("Giriş Yap", on_click=cb_giris_yap)
    if st.session_state['login_error']: st.sidebar.error("Hatalı Şifre!")
    st.title("Lojistik Pazar Yeri")
    st.info("Sol menüden giriş yapınız.")
    resim_url = "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?q=80&w=1000&auto=format&fit=crop"
    st.markdown(f'<img src="{resim_url}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
else:
    rol = st.session_state['aktif_rol']
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.sidebar.success(f"👤 {rol}")
    st.sidebar.markdown("---")
    st.sidebar.button("⬅️ Geri Dön", on_click=cb_cikis_yap)

    if rol == "Nakliyeci Girişi":
        st.header("📦 İlan Girişi")
        if 'form_msg' in st.session_state:
            tur, msg = st.session_state['form_msg']
            if tur == "error": st.error(msg)
            else: st.success(msg)
            del st.session_state['form_msg']

        main_c1, main_c2 = st.columns([3, 1])

        with main_c2:
            st.info("👇 Rota Kapsamı Seç")
            st.markdown("### 🌍 Kapsam")
            kapsam = st.radio("Rota Türü:", 
                              ["Yurt İçi", "Uluslararası", "İhracat (TR->EU)", "İthalat (EU->TR)"], 
                              horizontal=False, 
                              key="n_kapsam")
            st.markdown("---")
            st.caption("Seçiminize göre şehir listeleri solda otomatik güncellenecektir.")

        nereden_liste = ["Seçiniz..."]
        nereye_liste = ["Seçiniz..."]
        if kapsam == "Yurt İçi":
            nereden_liste += turkiye_illeri; nereye_liste += turkiye_illeri
        elif kapsam == "Uluslararası":
            nereden_liste += avrupa_ulkeleri; nereye_liste += avrupa_ulkeleri
        elif kapsam == "İhracat (TR->EU)":
            nereden_liste += turkiye_illeri; nereye_liste += avrupa_ulkeleri
        elif kapsam == "İthalat (EU->TR)":
            nereden_liste += avrupa_ulkeleri; nereye_liste += turkiye_illeri

        with main_c1:
            with st.form("ilan_formu"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    st.text_input("Firma Adı", key="n_ad")
                    st.text_input("İletişim", key="n_tel")
                    st.selectbox("Nereden", nereden_liste, key="n_nereden")
                    st.selectbox("Nereye", nereye_liste, key="n_nereye")
                    st.text_area("Notlar", key="n_not")
                
                with fc2:
                    st.text_input("📦 Yük Cinsi", key="n_yuk")
                    # min_value=0.0 yaparak sayı giriş limitini kaldırdık
                    st.number_input("Tonaj", min_value=0.0, value=1.0, key="n_ton")
                    st.selectbox("Para Birimi", ["TL", "USD", "EUR", "GBP"], key="n_birim")
                    # min_value=0 yaparak 2000 sınırını kaldırdık
                    st.number_input("Müşteriden Alınan Fiyat", min_value=0, value=2000, key="n_satis")
                    st.number_input("Şoföre Ödenecek Fiyat", min_value=0, value=1500, key="n_ucret")
                    st.number_input("Süre (Saat)", min_value=0, value=24, key="n_sure")
                
                st.markdown("---")
                st.form_submit_button("🚀 İlanı Yayınla", on_click=cb_ilan_yayinla)

    elif rol == "Şoför Girişi":
        st.title("🚛 Yük Arama")
        tab1, tab2 = st.tabs(["🔍 Yük Bul", "🚛 Yüklerim"])
        with tab1:
            df = st.session_state.ilanlar
            aktif = df[df["Durum"] == "Aktif"].copy()
            if not aktif.empty:
                st.dataframe(aktif[["ID", "Yük_Tipi", "Nereden", "Nereye", "Ücret", "Para_Birimi"]], use_container_width=True)
                st.markdown("---")
                secilen_id = st.selectbox("İş ID Seç:", aktif["ID"].tolist())
                secilen_is = aktif[aktif["ID"] == secilen_id].iloc[0]
                
                st.markdown(f"### 📍 Rota: {secilen_is['Nereden']} -> {secilen_is['Nereye']}")
                
                sc = SEHIR_KOORDINATLARI.get(secilen_is['Nereden'])
                ec = SEHIR_KOORDINATLARI.get(secilen_is['Nereye'])
                
                if sc and ec:
                    mesafe = mesafe_hesapla(sc, ec)
                    st.info(f"📏 Kuş Uçuşu Tahmini Mesafe: **{mesafe:.0f} km**")
                    m = folium.Map(location=[(sc[0]+ec[0])/2, (sc[1]+ec[1])/2], zoom_start=5)
                    folium.Marker(sc, tooltip="Başlangıç", icon=folium.Icon(color="green", icon="play")).add_to(m)
                    folium.Marker(ec, tooltip="Varış", icon=folium.Icon(color="red", icon="flag")).add_to(m)
                    folium.PolyLine([sc, ec], color="blue", weight=2.5).add_to(m)
                    st_folium(m, width=700, height=250)
                    
                    maps_url = f"https://www.google.com/maps/dir/{secilen_is['Nereden']}/{secilen_is['Nereye']}/gas+stations"
                    st.link_button("⛽ Navigasyon, Benzinlik ve Tesisleri Gör (Google Maps)", maps_url)
                
                # --- YEŞİL KUTU BURADAN KALDIRILDI ---
                
                st.divider()
                mevcut = st.session_state.basvurular.get(secilen_id)
                durum = mevcut["status"] if mevcut else "Yok"
                
                if durum == "Yok":
                    c1, c2 = st.columns(2)
                    st.file_uploader("Ehliyet", type=['png','jpg'], key=f"ehliyet_{secilen_id}")
                    st.camera_input("Foto", key=f"foto_{secilen_id}")
                    st.button("📤 Başvur", on_click=cb_basvuru_yap, args=(secilen_id,))
                elif durum == "Bekliyor": st.info("⏳ Onay bekleniyor...")
                elif durum == "Onaylandi":
                    st.success("🎉 Başvurunuz ONAYLANDI!")
                    st.button("🚀 İşi Al", on_click=cb_isi_kabul_et, args=(secilen_id,))
            else: st.warning("Aktif yük bulunamadı.")
        with tab2:
            alinan = df[df["Durum"] == "Alındı"]
            if not alinan.empty:
                for i, row in alinan.iterrows():
                    st.info(f"Yolda: {row['Yük_Tipi']} ({row['Nereden']} -> {row['Nereye']}) - {row['Ücret']} {row['Para_Birimi']}")
                    maps_url = f"https://www.google.com/maps/dir/{row['Nereden']}/{row['Nereye']}/gas+stations"
                    st.link_button("🗺️ Yol Tarifi Al", maps_url)
                    st.button(f"🏁 Teslim Et (ID: {row['ID']})", key=f"btn_teslim_{row['ID']}", on_click=cb_teslim_et, args=(i,))
            else: st.info("İş yok.")

    elif rol == "Yönetici Girişi":
        st.title("🔧 Yönetici Paneli")
        tab_rapor, tab_onay, tab_arsiv = st.tabs(["📊 Raporlar", "📝 Onaylar", "🗂️ Dosyalar"])
        with tab_rapor:
            st.markdown("### 📈 Finansal Özet")
            df = st.session_state.ilanlar
            if not df.empty:
                gelir_ozeti = df.groupby("Para_Birimi")["Satis_Fiyati"].sum()
                gider_ozeti = df.groupby("Para_Birimi")["Ücret"].sum()
                kar_ozeti = gelir_ozeti.sub(gider_ozeti, fill_value=0)
                
                gelir_str = " + ".join([f"{val:,.0f} {cur}" for cur, val in gelir_ozeti.items()])
                gider_str = " + ".join([f"{val:,.0f} {cur}" for cur, val in gider_ozeti.items()])
                kar_str = " + ".join([f"{val:,.0f} {cur}" for cur, val in kar_ozeti.items()])
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Toplam Ciro", gelir_str if gelir_str else "0")
                m2.metric("Toplam Şoför Ödemesi", gider_str if gider_str else "0")
                m3.metric("Toplam Net Kâr", kar_str if kar_str else "0")
                
                st.divider()
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Excel İndir", csv, "lojistik_rapor.csv", "text/csv")
            else: st.info("Veri yok.")
            st.markdown("---")
            st.button("🚨 SİSTEMİ SIFIRLA", on_click=cb_sistemi_sifirla)

        with tab_onay:
            bekleyenler = [k for k,v in st.session_state.basvurular.items() if v["status"] == "Bekliyor"]
            if not bekleyenler: st.info("Onay bekleyen yok.")
            for pid in bekleyenler:
                basvuru = st.session_state.basvurular[pid]
                st.write(f"**Başvuru ID:** {pid}")
                c1, c2, c3 = st.columns(3)
                with c1: st.image(basvuru["ehliyet"], width=150)
                with c2: st.image(basvuru["foto"], width=150)
                with c3:
                    st.button("✅ ONAYLA", key=f"onay_{pid}", on_click=cb_yonetici_onay, args=(pid,))
                    st.button("❌ REDDET", key=f"red_{pid}", on_click=cb_yonetici_red, args=(pid,))
                st.divider()

        with tab_arsiv:
            st.markdown("### 🗄️ Arşiv")
            arsiv_var_mi = False
            for pid, veri in st.session_state.basvurular.items():
                if veri["status"] in ["Onaylandi", "Tamamlandı"]:
                    arsiv_var_mi = True
                    is_detayi = st.session_state.ilanlar[st.session_state.ilanlar["ID"] == pid]
                    baslik = f"Dosya #{pid} - Durum: {veri['status']}"
                    if not is_detayi.empty: baslik += f" | {is_detayi.iloc[0]['Nakliyeci']}"
                    with st.expander(baslik):
                        ac1, ac2 = st.columns(2)
                        with ac1: st.image(veri["ehliyet"], width=200, caption="Ehliyet")
                        with ac2: st.image(veri["foto"], width=200, caption="Şoför")
            if not arsiv_var_mi: st.info("Arşiv boş.")
"""

with open("lojistik_proje_final_v25.py", "w", encoding="utf-8") as f:
    f.write(dosya_icerigi)

print("✅ Güncelleme tamamlandı: lojistik_proje_final_v25.py")
print("🛠️ SİSTEM: Yeşil kutu kaldırıldı. Sayı girişlerindeki '2000' limiti (min_value) düzeltildi.")
print("🚀 Sistem başlatılıyor...")
try:
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", "lojistik_proje_final_v25.py"])
    time.sleep(3)
except Exception as e:
    print(f"Hata: {e}")