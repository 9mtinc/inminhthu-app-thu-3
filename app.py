import streamlit as st
import pandas as pd
import datetime
from datetime import datetime as dt, time
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

thu_map = {
    0: "Thứ hai", 1: "Thứ ba", 2: "Thứ tư", 3: "Thứ năm",
    4: "Thứ sáu", 5: "Thứ bảy", 6: "Chủ nhật"
}

menu = [
    {"Loại nước": "Bạc xỉu", "Size": "500ml", "Giá bán": 17000, "Chi phí": 5177},
    {"Loại nước": "Cà phê muối", "Size": "500ml", "Giá bán": 16000, "Chi phí": 1722},
    {"Loại nước": "Cà phê sữa", "Size": "500ml", "Giá bán": 15000, "Chi phí": 3759},
    {"Loại nước": "Cà phê đen", "Size": "500ml", "Giá bán": 12000, "Chi phí": 3535},
    {"Loại nước": "Matcha latte", "Size": "500ml", "Giá bán": 17000, "Chi phí": 6584},
    {"Loại nước": "Trà tắc", "Size": "500ml", "Giá bán": 8000, "Chi phí": 3809},
    {"Loại nước": "Trà đường", "Size": "500ml", "Giá bán": 6000, "Chi phí": 2189},
]

df_menu = pd.DataFrame(menu)
excel_file = "don_hang.xlsx"

if os.path.exists(excel_file):
    orders = pd.read_excel(excel_file)
else:
    orders = pd.DataFrame(columns=["Khách", "Thời gian", "Món", "Size", "Số lượng", "Doanh thu", "Chi phí", "Lợi nhuận"])

if "orders" not in st.session_state:
    st.session_state.orders = orders

st.title("INMINH CAFÉ ☕ - QUẢN LÍ DOANH THU")

with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        ten_khach = st.text_input("Tên khách hàng", value=st.session_state.get("ten_khach", ""), key="ten_khach")
        ngay_mua = st.date_input("Ngày mua", value=st.session_state.get("ngay_mua", dt.today().date()), key="ngay_mua")
    with col2:
        gio_mua = st.time_input(
            "Giờ mua",
            value=st.session_state.get("gio_mua", time(8, 0)),
            step=datetime.timedelta(minutes=1),
            key="gio_mua"
        )

    thoi_gian = dt.combine(ngay_mua, gio_mua)
    thu = thu_map[thoi_gian.weekday()]
    thoi_gian_str = f"{thu}, {thoi_gian.strftime('%d/%m/%Y %H:%M')}"

    loai_nuoc = st.selectbox("Loại nước", df_menu["Loại nước"].unique(), index=0, key="loai_nuoc")
    size = st.selectbox("Size", df_menu[df_menu["Loại nước"] == loai_nuoc]["Size"].unique(), index=0, key="size")
    so_luong = st.number_input("Số lượng", min_value=1, value=1, key="so_luong")

    submit = st.form_submit_button("➕ Thêm đơn hàng")

    if submit and ten_khach:
        row = df_menu[(df_menu["Loại nước"] == loai_nuoc) & (df_menu["Size"] == size)].iloc[0]
        doanh_thu = row["Giá bán"] * so_luong
        chi_phi = row["Chi phí"] * so_luong
        loi_nhuan = doanh_thu - chi_phi

        new_order = pd.DataFrame([{
            "Khách": ten_khach,
            "Thời gian": thoi_gian_str,
            "Món": loai_nuoc,
            "Size": size,
            "Số lượng": so_luong,
            "Doanh thu": doanh_thu,
            "Chi phí": chi_phi,
            "Lợi nhuận": loi_nhuan
        }])
        st.session_state.orders = pd.concat([st.session_state.orders, new_order], ignore_index=True)
        st.session_state.orders.to_excel(excel_file, index=False)

        for key in ["ten_khach", "ngay_mua", "gio_mua", "loai_nuoc", "size", "so_luong"]:
            if key in st.session_state:
                del st.session_state[key]

        st.success("✅ Đã thêm đơn và reset form!")
        st.rerun()

# --- BẢNG LỊCH SỬ ---
st.subheader("📦 Lịch sử đơn hàng")
st.dataframe(st.session_state.orders, use_container_width=True)

# --- TẢI FILE EXCEL ---
st.subheader("⬇️ Tải đơn hàng Excel")
if os.path.exists(excel_file):
    with open(excel_file, "rb") as f:
        st.download_button("📥 Tải file Excel", f, file_name="don_hang.xlsx")
else:
    st.info("📂 Chưa có đơn hàng nào được lưu để tải về.")

# --- THỐNG KÊ ---
df = st.session_state.orders
if not df.empty:
    st.subheader("📊 Thống kê")
    st.metric("Tổng doanh thu", f"{df['Doanh thu'].sum():,} VND")
    st.metric("Tổng lợi nhuận", f"{df['Lợi nhuận'].sum():,} VND")
    st.metric("Tổng số ly bán", int(df["Số lượng"].sum()))

    st.bar_chart(df.groupby("Thời gian")["Doanh thu"].sum())

    pie = df.groupby("Món")["Số lượng"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie, labels=pie.index, autopct='%1.1f%%', startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

# --- XOÁ ĐƠN ---
st.subheader("🗑 Xóa đơn hàng sai")
if not df.empty:
    for idx, row in df.iterrows():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"{idx+1}. {row['Khách']} - {row['Món']} {row['Size']} ({row['Số lượng']} ly) - {row['Thời gian']}")
        with col2:
            if st.button("🗑 Xóa", key=f"delete_{idx}"):
                st.session_state.orders.drop(index=idx, inplace=True)
                st.session_state.orders.reset_index(drop=True, inplace=True)
                st.session_state.orders.to_excel(excel_file, index=False)
                st.success("✅ Đã xóa đơn và cập nhật Excel.")
                st.rerun()
