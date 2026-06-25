import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Cấu hình trang
st.set_page_config(page_title="App Quản Lý Khuôn", layout="wide")
st.title("🏭 QUẢN LÝ KHUÔN - PHÂN XƯỞNG")

# 2. Kết nối Google Sheets (Dùng st.cache_resource để không phải kết nối lại nhiều lần)
@st.cache_resource
def connect_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # Trên Streamlit Cloud, bạn sẽ lưu JSON trong Secrets
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open_by_key(st.secrets["sheet_id"]).sheet1

sheet = connect_sheets()
data = sheet.get_all_records()

# 3. Giao diện lọc dữ liệu
col1, col2 = st.columns(2)
with col1:
    zone = st.selectbox("Chọn Zone", [1, 2, 3, 4, 5, 6, 7])
with col2:
    may = st.selectbox("Chọn Máy", [1, 2, 3, 4, 5, 6])

# 4. Hiển thị dữ liệu đã lọc
filtered_data = [row for row in data if row['Zone'] == zone and row['Máy'] == may]

if filtered_data:
    st.subheader(f"Kết quả: Zone {zone} - Máy {may}")
    st.table(filtered_data) # Hiển thị dạng bảng trực quan
else:
    st.warning("Không tìm thấy dữ liệu cho Zone và Máy này!")
