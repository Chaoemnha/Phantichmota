import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Đọc file CSV
file_path = "historical_air_quality_2021_en.csv"  # Thay bằng đường dẫn file CSV
data = pd.read_csv(file_path)

# Loại bỏ các dòng hoàn toàn trống
data = data.dropna(how="all")

# Chuyển đổi các giá trị đặc biệt thành NaN
data.replace(["-", "", "#NAME?"], pd.NA, inplace=True)

# Kiểm tra dữ liệu bị khuyết
missing_data = data.isnull().sum()
missing_percentage = (missing_data / len(data)) * 100

# Xử lý dữ liệu khuyết
threshold = 30  # Ngưỡng phần trăm
columns_to_drop = missing_percentage[missing_percentage > threshold].index
data_cleaned = data.drop(columns=columns_to_drop)

# Chuyển đổi các giá trị sai về đúng định dạng (Tiền xử lý dữ liệu)
data_cleaned["Data Time S"] = pd.to_datetime(data_cleaned['Data Time S'])
data_cleaned["AQI index"] = pd.to_numeric(data_cleaned['AQI index'])
data_cleaned["Pressure"] = pd.to_numeric(data_cleaned['Pressure'].str.replace(',', ''))
data_cleaned["CO"] = pd.to_numeric(data_cleaned['CO'])
data_cleaned["NO2"] = pd.to_numeric(data_cleaned['NO2'])
data_cleaned["PM10"] = pd.to_numeric(data_cleaned['PM10'])
data_cleaned["PM2.5"] = pd.to_numeric(data_cleaned['PM2.5'])

# Thay thế giá trị khuyết trong các cột còn lại
data_cleaned.fillna({
    "AQI index": data_cleaned["AQI index"].median(),  # Thay bằng giá trị trung vị
    "Humidity": data_cleaned["Humidity"].median(),
    "Pressure": data_cleaned["Pressure"].median(),
    "Temperature": data_cleaned["Temperature"].median(),
    "Wind": data_cleaned["Wind"].median(),
    "CO": data_cleaned["CO"].mean(),  # Thay bằng giá trị trung bình
    "Dew": data_cleaned["Dew"].mean(),
    "NO2": data_cleaned["NO2"].mean(),
    "PM10": data_cleaned["PM10"].mean(),
    "PM2.5": data_cleaned["PM2.5"].mean(),
    "Dominent pollutant": "Not Specified",
}, inplace=True)


# Tạo giao diện Streamlit
def main():
    st.title("Phân tích Dữ liệu Ô nhiễm Không khí")
    st.sidebar.header("Công cụ phân tích")

    # Các lựa chọn menu
    analysis_option = st.sidebar.selectbox("Chọn phân tích",
                                           ["Thống kê mô tả",
                                            "Biểu đồ phân bố",
                                            "Ma trận tương quan",
                                            "Biểu đồ phân tán"])

    # Tạo thống kê mô tả
    if analysis_option == "Thống kê mô tả":
        st.subheader("Thống kê mô tả về các biến")
        descriptive_stats = data_cleaned[
            ['AQI index', 'CO', 'Dew', 'Humidity', 'NO2', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']].describe(
            percentiles=[0.25, 0.5, 0.75])
        st.write(descriptive_stats)

    # Phân tích biểu đồ phân bố
    elif analysis_option == "Biểu đồ phân bố":
        st.subheader("Phân bố của các biến")
        fig, axes = plt.subplots(3, 4, figsize=(15, 10))
        axes = axes.ravel()

        numeric_columns = ['AQI index', 'CO', 'Dew', 'Humidity', 'NO2', 'Pressure', 'PM10', 'PM2.5', 'Temperature',
                           'Wind']

        for i, col in enumerate(numeric_columns):
            axes[i].hist(data_cleaned[col].dropna(), bins=20, edgecolor='black')
            axes[i].set_title(f'Phân Bố {col}')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Tần Suất')

        st.pyplot(fig)

    # Phân tích ma trận tương quan
    elif analysis_option == "Ma trận tương quan":
        st.subheader("Ma trận tương quan các biến")
        correlation_matrix = data_cleaned[
            ['AQI index', 'CO', 'Dew', 'Humidity', 'NO2', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Biểu đồ phân tán 2 chiều
    elif analysis_option == "Biểu đồ phân tán":
        st.subheader("Biểu đồ phân tán")
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.ravel()

        axes[0].scatter(data_cleaned['PM2.5'], data_cleaned['AQI index'])
        axes[0].set_title('PM2.5 vs AQI Index')
        axes[0].set_xlabel('PM2.5')
        axes[0].set_ylabel('AQI Index')

        axes[1].scatter(data_cleaned['Temperature'], data_cleaned['AQI index'])
        axes[1].set_title('Temperature vs AQI Index')
        axes[1].set_xlabel('Temperature')
        axes[1].set_ylabel('AQI Index')

        st.pyplot(fig)


if __name__ == "__main__":
    main()

#streamlit run Demo.py