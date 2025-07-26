import streamlit as st
import pandas as pd
from datetime import datetime, time
import matplotlib.pyplot as plt

# Load menu
menu = [
    {"Loại nước": "Bạc xỉu", "Size": "500ml", "Giá bán": 17000, "Chi phí": 5177},
    {"Loại nước": "Bạc xỉu", "Size": "800ml", "Giá bán": 22000, "Chi phí": 7404},
    {"Loại nước": "Bạc xỉu", "Size": "1 lít", "Giá bán": 27000, "Chi phí": 9842},
    {"Loại nước": "Cà phê muối", "Size": "500ml", "Giá bán": 16000, "Chi phí": 1722},
    {"Loại nước": "Cà phê muối", "Size": "800ml", "Giá bán": 21000, "Chi phí": 1776},
    {"Loại nước": "Cà phê muối", "Size": "1 lít", "Giá bán": 26000, "Chi phí": 2041},
    {"Loại nước": "Cà phê sữa", "Size": "500ml", "Giá bán": 15000, "Chi phí": 3759},
    {"Loại nước": "Cà phê sữa", "Size": "800ml", "Giá bán": 19000, "Chi phí": 4569},
    {"Loại nước": "Cà phê sữa", "Size": "1 lít", "Giá bán": 23000, "Chi phí": 5824},
    {"Loại nước": "Cà phê đen", "Size": "500ml", "Giá bán": 12000, "Chi phí": 3535},
    {"Loại nước": "Cà phê đen", "Size": "800ml", "Giá bán": 17000, "Chi phí": 4409},
    {"Loại nước": "Cà phê đen", "Size": "1 lít", "Giá bán": 20000, "Chi phí": 5261},
    {"Loại nước": "Matcha latte", "Size": "500ml", "Giá bán": 17000, "Chi phí": 6584},
    {"Loại nước": "Matcha latte", "Size": "800ml", "Giá bán": 22000, "Chi phí": 9311},
    {"Loại nước": "Matcha latte", "Size": "1 lít", "Giá bán": 26000, "Chi phí": 12959},
    {"Loại nước": "Matcha latte", "Size": "500ml", "Giá bán": 19000, "Chi phí": 1722},
    {"Loại nước": "Matcha latte", "Size": "800ml", "Giá bán": 24000, "Chi phí": 1776},
    {"Loại nước": "Matcha latte", "Size": "1 lít", "Giá bán": 28000, "Chi phí": 2041},
    {"Loại nước": "Trà tắc", "Size": "500ml", "Giá bán": 8000, "Chi phí": 3809},
    {"Loại nước": "Trà tắc", "Size": "800ml", "Giá bán": 10000, "Chi phí": 4535},
    {"Loại nước": "Trà tắc", "Size": "1 lít", "Giá bán": 15000, "Chi phí": 6072},
    {"Loại nước": "Trà đường", "Size": "500ml", "Giá bán": 6000, "Chi phí": 2189},
    {"Loại nước": "Trà đường", "Size": "800ml", "Giá bán": 9000, "Chi phí": 2435},
    {"Loại nước": "Trà đường", "Size": "1 lít", "Giá bán": 10000, "Chi phí": 2892},
]

df_menu = pd.DataFrame(menu)

# Khởi tạo session state
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=["Khách", "Thời gian", "Món", "Size", "Số lượng", "Doanh thu", "Chi phí", "Lợi nhuận"])

st.title("INMINH CAFÉ - QUẢN LÍ DOANH THU")

# --- Nhập thông tin khách ---
with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        ten_khach = st.text_input("Tên khách hàng")
        ngay_mua = st.date_input("Ngày mua")
    with col2:
        gio_mua = st.time_input("Giờ mua", value=time(8, 0), step=60)  # step=60 giây -> chọn từng phút

    thoi_gian = datetime.combine(ngay_mua, gio_mua)

    loai_nuoc = st.selectbox("Loại nước", df_menu["Loại nước"].unique())
    size = st.selectbox("Size", df_menu[df_menu["Loại nước"] == loai_nuoc]["Size"].unique())
    so_luong = st.number_input("Số lượng", min_value=1, value=1)

    submit = st.form_submit_button("Thêm đơn hàng")
    if submit and ten_khach:
        row = df_menu[(df_menu["Loại nước"] == loai_nuoc) & (df_menu["Size"] == size)].iloc[0]
        doanh_thu = row["Giá bán"] * so_luong
        chi_phi = row["Chi phí"] * so_luong
        loi_nhuan = doanh_thu - chi_phi

        new_order = pd.DataFrame([{
            "Khách": ten_khach,
            "Thời gian": thoi_gian,
            "Món": loai_nuoc,
            "Size": size,
            "Số lượng": so_luong,
            "Doanh thu": doanh_thu,
            "Chi phí": chi_phi,
            "Lợi nhuận": loi_nhuan
        }])
        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
        st.success("✅ Đã thêm đơn hàng mới!")
        st.experimental_rerun()

# --- Hiển thị lịch sử ---
st.subheader("📦 Lịch sử đơn hàng")
st.dataframe(st.session_state.orders, use_container_width=True)

# --- Thống kê tổng hợp ---
st.subheader("📊 Thống kê")
df = st.session_state.orders
if not df.empty:
    tong_doanh_thu = df["Doanh thu"].sum()
    tong_loi_nhuan = df["Lợi nhuận"].sum()
    tong_chi_phi = df["Chi phí"].sum()
    tong_so_ly = df["Số lượng"].sum()

    st.metric("Tổng doanh thu", f"{tong_doanh_thu:,} VND")
    st.metric("Tổng lợi nhuận", f"{tong_loi_nhuan:,} VND")
    st.metric("Tổng số ly bán", tong_so_ly)

    # Biểu đồ cột doanh thu theo ngày
    doanh_thu_ngay = df.groupby(df["Thời gian"].dt.date)["Doanh thu"].sum()
    st.bar_chart(doanh_thu_ngay)

    # Biểu đồ tròn món bán ra
    df_pie = df.groupby("Món")["Số lượng"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(df_pie, labels=df_pie.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
