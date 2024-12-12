import streamlit as st
import requests

# Tiêu đề ứng dụng
st.title("Translator App")

# Khởi tạo trạng thái
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Thêm lựa chọn chế độ dịch
mode = st.radio("Select translation mode:", ["English to Vietnamese", "Vietnamese to English"])

# Nhập văn bản từ người dùng
input_text = st.text_area("Enter text to translate:", "")


# Xử lý nút Translate
def translate_action():
    st.session_state.button_clicked = True


st.button("Translate", on_click=translate_action)

# Kiểm tra trạng thái nút và thực hiện yêu cầu API
if st.session_state.button_clicked:
    if input_text.strip():
        try:
            # Xác định hướng dịch dựa trên chế độ
            direction = "vi-en" if mode == "Vietnamese to English" else "en-vi"

            # Gọi API
            response = requests.post(
                "http://127.0.0.1:8000/translate",
                json={"text": input_text,
                      "translation_from_to": direction}  # Thêm hướng dịch vào payload
            )

            # Kiểm tra phản hồi từ API
            if response.status_code == 200:
                translated_text = response.json().get('Translated text')
                st.success(f'{translated_text}')
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter text to translate.")
    # Reset trạng thái nút
    st.session_state.button_clicked = False
