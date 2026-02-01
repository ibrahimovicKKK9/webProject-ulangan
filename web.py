import streamlit as st
import mysql.connector as conn

#Variable
#Register - Login
nis = 0
Nama_Lengkap = "Ibrahimovic Kurniawan (DEVELOPER)"
Username = ""
Password = ""

# Fungsi untuk koneksi ke Database
def buat_koneksi():
    return conn.connect(
        host="localhost",
        user="root",
        password="",
        database="ulangan_test"
    )

# Fungsi untuk Validasi Login
def login_user(username_input, password_input):
    conn = buat_koneksi()
    cursor = conn.cursor(dictionary=True) # Agar hasil berupa dict: user['nama_lengkap']
    
    query = "SELECT * FROM akun WHERE Username = %s AND Password = %s"
    cursor.execute(query, (username_input, password_input))
    user = cursor.fetchone() # Ambil satu baris data saja
    
    conn.close()
    return user # Mengembalikan data user jika ada, atau None jika tidak ada

def simpan_user(nis, nama, username, password):
    conn = buat_koneksi()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO akun (NIS, `Nama Lengkap`, Username, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nis, nama, username, password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Gagal simpan: {e}")
        return False
    finally:
        conn.close()

def cek_akun(nis):
    conn = buat_koneksi()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM akun WHERE NIS = %s"
    cursor.execute(query, (nis,))
    akun = cursor.fetchone()

    conn.close()
    return akun



# --- UI SETUP ---
st.set_page_config(page_title="SMKN2UJIAN", layout="wide")

if not "page" in st.session_state:
    st.session_state["page"] = "Utama"

left_spacer, center_column, right_spacer = st.columns([1, 2, 1])

with center_column:
    
    if st.session_state["page"] == "Utama":
        tab_home, tab_login, tab_reg = st.tabs(["🏠 Welcome", "🔐 Login", "📝 Register"])

        with tab_home:
            st.header("Selamat Datang, Semangat Ujian")
            st.write("SMKN 2 KOTA BEKASI")
            st.divider()
            st.info("Semua sistem yang ada sedang dalam proses perkembangan. Mohon Ditunggu")


        with tab_login:
            st.header("👤 Panel Account Login")
            st.write("Jika sudah memiliki account, kamu bisa masukan Username berserta Passwordnya.\nJika belum silahkan bisa melakukan pendaftaran/Register")
            st.divider()
            input_username = st.text_input("Username:")
            input_password = st.text_input("Password:", type="password")
            left, right = st.columns([1, 5])
            if left.button("🚀 Login", key="btn_login"):
                user_data = login_user(input_username, input_password)
                if user_data:
                    st.session_state["page"] = "Beranda"
                    st.experimental_rerun()
                elif input_username == "" or input_password == "":
                    st.error("Tolong jangan kosongkan, silahkan isi semua data yang ada")
                else:
                    st.error("Username atau Password salah")
            if right.button("🔑 Lupa Password?", key="btn_lupa_password"):
                st.session_state["page"] = "LupaPassword"
                st.experimental_rerun()

        with tab_reg:
            st.header("👤 Panel Account Register")
            st.write("Register lah buat akun lah bodoh buat ulangan yaampun")
            st.divider()
            input_nis = st.text_input("NIS:")
            input_nama_lengkap = st.text_input("Nama Lengkap:")
            input_username = st.text_input("Username:", key="input_username")
            input_password =  st.text_input("Password:", type="password", key="input_password")
            input_confirm_password =st.text_input("Confirm Password:", type="password", key="input_confirm_password")
            if st.button("👤 Create Account"):
                if cek_akun(input_nis):
                    st.info("Kamu sudah memiliki account, tidak membuat akun lagi")
                elif input_nis == "" or input_nama_lengkap == "" or input_username == "" or input_password == "" or input_confirm_password == "":
                    st.error("Tolong jangan kosongkan, silahkan isi semua data yang ada")
                elif input_confirm_password != input_password:
                    st.error("Konfirmasi Password tidak cocok dengan Passwordmu, silahkan dicek kembali")
                else:
                    simpan_user(input_nis, input_nama_lengkap, input_username, input_password)
                    st.session_state["page"] = "Beranda"
                    st.success("Account kamu berhasil terbuat. silahkan lakukan login agar bisa mengikuti Ulangan. Semangat!!")
                    st.experimental_rerun()
        

    elif st.session_state["page"] == "LupaPassword":
        st.header("🔑 Lupa Password")
        st.write("Nenek/Kakek pw aja lupa dasar PIKUN!!")
        st.divider()
        input_new_password = st.text_input("Password Baru:", type="password")
        input_konfirm_new_password = st.text_input("Konfirmasi Password:", type="password")
        if st.button("🚀 Ganti Password"):
            if input_new_password == "" or input_konfirm_new_password == "":
                st.error("Tolong jangan kosongkan, silahkan isi semua data yang ada")
            elif input_konfirm_new_password != input_new_password:
                st.error("Pasword Konfirmasi tidak sama dengan Password Baru kamu.")
            else:
                conn = buat_koneksi()
                cursor = conn.cursor()
                query = "UPDATE akun SET Password = %s WHERE akun . NIS = %s"
                cursor.execute(query, (input_new_password, nis))
                conn.commit()

                st.session_state["page"] = "Utama"
                st.success("Berhasil ganti password, silahkan login kembali")
                st.experimental_rerun()


    elif st.session_state["page"] == "Beranda":
        tab_beranda, tab_jadwal_ulangan, tab_ulangan, tab_panel_akun = st.tabs(["🏠 Beranda", "📅 Jadwal Ulangan", "📝 Ulangan", "👤 Account Settings"])

        with tab_beranda:
            st.header("🏠 Beranda")
            st.write(f"Selamat datang, {Nama_Lengkap}. Disini akan ada informasi jika ada perubahan jadwal atau perbaruan apapun. SEMANGAT UJIAN!!")
            st.divider()
            st.info("Waiting...")
        
        with tab_jadwal_ulangan:
            st.header("📅 Jadwal Ulangan")
            st.divider()
            with st.expander("📆 **SENIN 6 Juli 2026**"):
                col1, col2 = st.columns([1, 1])
                col1.write("📒 Mata Pelajaran: INFORMATIKA")
                col2.write("⏱ Waktu Ulangan: 07.00 - 12.20 WIB")
            with st.expander("📆 **SELASA 7 Juli 2026**"):
                col1, col2 = st.columns([2, 1])
                col1.write("📒 Mata Pelajaran: KKA (Coding dan AI)")
                col1.write("📒 Mata Pelajaran: DASJUR (Dasar Jurusan)")
                col2.write("⏱ Waktu Ulangan: 07.00 - 12.00 WIB")
                col2.write("⏱ Waktu Ulangan: 12.00 - 14.40 WIB")
            with st.expander("📆 **RABU 8 Juli 2026**"):
                col1, col2 = st.columns([2, 1])
                col1.write("📒 Mata Pelajaran: DASJUR (Dasar Jurusan)")
                col2.write("⏱ Waktu Ulangan: 07.00 - 12.20 WIB")
            with st.expander("📆 **KAMIS 9 Juli 2026**"):
                col1, col2 = st.columns([2, 1])
                col1.write("📒 Mata Pelajaran: DASJUR (Dasar Jurusan)")
                col1.write("📒 Mata Pelajaran: IPAS")
                col2.write("⏱ Waktu Ulangan: 07.00 - 12.00 WIB")
                col2.write("⏱ Waktu Ulangan: 12.00 - 14.40 WIB")
            with st.expander("📆 **JUMAT 10 Juli 2026**"):
                col1, col2 = st.columns([1, 1])
                col1.write("📒 Mata Pelajaran: IPAS")
                col2.write("⏱ Waktu Ulangan: 07.00 - 12.20 WIB")


        with tab_ulangan:
            st.header("📝 Ulangan")
            st.divider()

            with st.expander("📆 **SENIN 6 Juli 2026**"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write("📒 **Mata Pelajaran**")
                    st.write("💻 INFORMATIKA")
                    st.write("✅ **STATUS**: Online")
                with col2:
                    st.write("⏱ **Waktu Ulangan**")
                    st.write("07.00 - 12.20 WIB")
                with col3:
                    st.text_input("", placeholder="***", type="password", key="input_kode")
                    st.button("🟢 MASUK", key="btn_masuk")
            with st.expander("📆 **SELESA 7 Juli 2026**"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write("📒 **Mata Pelajaran**")
                    st.write("💻 KKA (Coding dan AI)")
                    st.write("💻 Dasjur (Dasar Jurusan)")
                    st.write("✅ **STATUS**: Online")
                with col2:
                    st.write("⏱ **Waktu Ulangan**")
                    st.write("07.00 - 12.00 WIB")
                    st.write("12.00 - 14.40 WIB")
                with col3:
                    st.text_input("", placeholder="***", type="password", key="input_kode2")
                    st.button("🟢 MASUK", key="btn_masuk2")
            with st.expander("📆 **RABU 8 Juli 2026**"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write("📒 **Mata Pelajaran**")
                    st.write("💻 Dasjur (Dasar Jurusan)")
                    st.write("✅ **STATUS**: Online")
                with col2:
                    st.write("⏱ **Waktu Ulangan**")
                    st.write("07.00 - 12.20 WIB")
                with col3:
                    st.text_input("", placeholder="***", type="password", key="input_kode3")
                    st.button("🟢 MASUK", key="btn_masuk3")
            with st.expander("📆 **KAMIS 9 Juli 2026**"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write("📒 **Mata Pelajaran**")
                    st.write("💻 Dasjur (Dasar Jurusan)")
                    st.write("🧬 IPAS")
                    st.write("✅ **STATUS**: Online")
                with col2:
                    st.write("⏱ **Waktu Ulangan**")
                    st.write("07.00 - 12.00 WIB")
                    st.write("12.00 - 14.40 WIB")
                with col3:
                    st.text_input("", placeholder="***", type="password", key="input_kode4")
                    st.button("🟢 MASUK", key="btn_masuk4")
            with st.expander("📆 **JUMAT 10 Juli 2026**"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write("📒 **Mata Pelajaran**")
                    st.write("🧬 IPAS")
                    st.write("✅ **STATUS**: Online")
                with col2:
                    st.write("⏱ **Waktu Ulangan**")
                    st.write("07.00 - 12.20 WIB")
                with col3:
                    st.text_input("", placeholder="***", type="password", key="input_kode5")
                    st.button("🟢 MASUK", key="btn_masuk5")


        with tab_panel_akun:
            st.header("👤 Account Settings")
            st.divider()
            st.subheader(f"Halo, {Nama_Lengkap}")
            st.write("Jika kamu memiliki masalah pada account kamu silah gunakan fitur yang ada di\nAccount Settings ini.")

            #-Lupa Password
            st.write("")
            st.write("Lupa Password:")
            if st.button("🔑 Lupa Password?"):
                st.session_state["page"] = "LupaPassword"
                st.experimental_rerun()
            st.warning("Saat kamu berhasil untuk mengganti Password kamu diwajibkan untuk Login ulang, jadi tolong diingat yaa..")

            #-Logout
            st.write("")
            st.write("Logout:")
            if st.button("🔴 Logout"):
                st.session_state["page"] = "Utama"
                st.experimental_rerun()
            st.error("Jika kamu keluar dari akun ini, kamu harus login ulang kembali")
            




