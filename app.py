import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Công Cụ Tính Lãi Tiết Kiệm")
st.write("So sánh tiền lãi thu được giữa **Lãi đơn** và **Lãi kép**.")

# Nhập dữ liệu từ người dùng
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ):", 
        min_value=1000, 
        value=100000000, 
        step=1000000, 
        format="%d"
    )
    
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):", 
        min_value=0.1, 
        max_value=20.0, 
        value=6.0, 
        step=0.1, 
        format="%.1f"
    )

with col2:
    so_thang_gui = st.number_input(
        "Số tháng gửi:", 
        min_value=1, 
        max_value=360, 
        value=12, 
        step=1
    )
    
    tan_suat_nhap_lai = st.selectbox(
        "Tần suất nhập lãi (cho lãi kép):",
        options=["Hàng tháng", "Hàng quý", "Hàng năm"]
    )

# Quy đổi tần suất nhập lãi sang số lần/năm (n)
map_tan_suat = {
    "Hàng tháng": 12,
    "Hàng quý": 4,
    "Hàng năm": 1
}
n = map_tan_suat[tan_suat_nhap_lai]

# Chuyển đổi thời gian gửi sang số năm
t_nam = so_thang_gui / 12

# --- CÔNG THỨC TÍNH TÁN ---
# 1. Lãi đơn
lai_don = so_tien_gui * (lai_suat_nam / 100) * t_nam
tong_tien_lai_don = so_tien_gui + lai_don

# 2. Lãi kép
# Công thức: A = P * (1 + r/n)^(n*t)
r = lai_suat_nam / 100
tong_tien_lai_kep = so_tien_gui * ((1 + r / n) ** (n * t_nam))
lai_kep = tong_tien_lai_kep - so_tien_gui

# --- HIỂN THỊ KẾT QUẢ ---
st.divider()
st.subheader("📊 Kết Quả Dự Tính")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown("### 🔹 Lãi Đơn")
    st.metric(label="Tiền lãi nhận được", value=f"{lai_don:,.0f} VNĐ")
    st.metric(label="Tổng số tiền nhận được", value=f"{tong_tien_lai_don:,.0f} VNĐ")

with res_col2:
    st.markdown("### 🔸 Lãi Kép")
    st.metric(
        label="Tiền lãi nhận được", 
        value=f"{lai_kep:,.0f} VNĐ", 
        delta=f"+{lai_kep - lai_don:,.0f} VNĐ (so với lãi đơn)"
    )
    st.metric(label="Tổng số tiền nhận được", value=f"{tong_tien_lai_kep:,.0f} VNĐ")

# --- BẢNG BẢNG SO SÁNH TỔNG QUAN ---
st.divider()
st.subheader("📋 Bảng So Sánh Chi Tiết")

data = {
    "Chỉ số": ["Vốn ban đầu", "Tiền lãi thu được", "Tổng tiền nhận về"],
    "Lãi đơn (VNĐ)": [f"{so_tien_gui:,.0f}", f"{lai_don:,.0f}", f"{tong_tien_lai_don:,.0f}"],
    "Lãi kép (VNĐ)": [f"{so_tien_gui:,.0f}", f"{lai_kep:,.0f}", f"{tong_tien_lai_kep:,.0f}"],
    "Chênh lệch (VNĐ)": ["0", f"{lai_kep - lai_don:,.0f}", f"{lai_kep - lai_don:,.0f}"]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)
