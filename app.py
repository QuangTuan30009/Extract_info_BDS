import streamlit as st
import ollama
import pandas as pd
import json
from io import BytesIO
from datetime import datetime

# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="Trích xuất thông tin BDS",
    page_icon="📥",
    layout="wide"
)

# =========================
# Header
# =========================
st.title("📥 Trích xuất thông tin Bất động sản (AI Powered)")
st.markdown("Ứng dụng sử dụng AI để trích xuất thông tin từ văn bản bất động sản sang định dạng JSON")
st.markdown("---")

# =========================
# Main Content
# =========================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Nhập thông tin bài đăng")

    user_input = st.text_area(
        label="Nội dung bài đăng bất động sản:",
        height=400,
        placeholder="Ví dụ:\nBán nhà mặt tiền Nguyễn Văn Linh, Q7\nDT: 5x20m, 3 tầng, 4PN, 5WC\nGiá: 15 tỷ\nSĐT: 0901234567",
        help="Dán toàn bộ nội dung bài đăng để trích xuất thông tin"
    )
    
    # Sample data button
    if st.button("📋 Dùng dữ liệu mẫu"):
        st.session_state.sample_text = """*** Giá < 5.79 tỷ TL > MS 989
😍 😍 😍 < P7- Gò Vấp> 😍 😍 😍
🚀 NHÀ ĐẸP ĐÓN TẾT 2026 !!
⚡ Vị trí : đường số 7, phường 7 củ ( nay là phường Hạnh Thông ) , đường trước nhà 3m thông Phan Văn Trị , Nguyễn Văn Nghị, Nguyễn Du. Giáp BT, PN, ngay chợ GV, đại học CN4, BV 175, ra sân bay 10p
⚡ DT : 3,5m x 14m . Sổ CN 48m2. Kết cấu 1trệt, 1 lầu
⚡ Nhà thiết kế full nội thất cao cấp với 3 PN ( co phòng ngủ trệt cho người già) , 4 toilet khép kín , ban công thoáng mát
👉 Sổ hồng chính chủ, bank duyệt cho vay 50% giá trị nhà.
💎 Giá: 5.79 tỷ thương lượng
Lh/ Việt 0907849789"""
        st.rerun()
    
    if 'sample_text' in st.session_state:
        user_input = st.session_state.sample_text
        del st.session_state.sample_text

    st.markdown("---")
    
    extract_button = st.button(
        "🚀 Trích xuất thông tin",
        type="primary",
        use_container_width=True
    )

with col2:
    st.subheader("📊 Kết quả")
    result_container = st.container()

# Processing
if extract_button:
    if not user_input.strip():
        st.warning("⚠️ Vui lòng nhập nội dung bài đăng trước!")
    else:
        with st.spinner("🤖 Đang trích xuất thông tin..."):
            try:
                # Extract JSON
                response = ollama.chat(
                    model="bds-pro",
                    messages=[{"role": "user", "content": user_input}]
                )

                model_output = response["message"]["content"]

                # Clean markdown
                if "```json" in model_output:
                    model_output = model_output.split("```json")[1].split("```")[0].strip()
                elif "```" in model_output:
                    model_output = model_output.split("```")[1].split("```")[0].strip()

                extracted_data = json.loads(model_output)

                with result_container:
                    st.success("✅ Trích xuất thành công!")

                    # TABLE
                    column_mapping = {
                        "so_nha": "Số nhà",
                        "duong": "Đường",
                        "phuong": "Phường",
                        "quan": "Quận",
                        "gia": "Giá",
                        "dien_tich": "Diện tích",
                        "sdt": "Số điện thoại",
                        "phong_ngu": "Phòng ngủ",
                        "wc": "WC",
                        "so_tang": "Số tầng",
                        "huong_nha": "Hướng nhà",
                        "huong_ban_cong": "Hướng ban công",
                        "phap_ly": "Pháp lý",
                        "co_ban_cong": "Có ban công",
                        "tien_ich": "Tiện ích"
                    }

                    df = pd.DataFrame([extracted_data])
                    df = df[[c for c in column_mapping if c in df.columns]]
                    df_display = df.rename(columns=column_mapping)

                    if "Tiện ích" in df_display.columns:
                        df_display["Tiện ích"] = df_display["Tiện ích"].apply(
                            lambda x: ", ".join(x) if isinstance(x, list) else str(x) if x else ""
                        )

                    if "Có ban công" in df_display.columns:
                        df_display["Có ban công"] = df_display["Có ban công"].apply(
                            lambda x: "✓ Có" if x is True or str(x).upper() == "CÓ" else "✗ Không"
                        )

                    st.dataframe(
                        df_display.T,
                        use_container_width=True,
                        column_config={
                            0: st.column_config.TextColumn("Thông tin", width="large")
                        }
                    )

                    # RAW JSON
                    with st.expander("🔍 Xem JSON"):
                        st.json(extracted_data)
                    
                    # Export buttons
                    col_dl1, col_dl2 = st.columns(2)
                    
                    with col_dl1:
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine="openpyxl") as writer:
                            df_display.to_excel(writer, index=False, sheet_name="BDS")
                        st.download_button(
                            "📥 Tải Excel",
                            data=output.getvalue(),
                            file_name=f"bds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    with col_dl2:
                        json_output = json.dumps(extracted_data, ensure_ascii=False, indent=2)
                        st.download_button(
                            "📥 Tải JSON",
                            data=json_output,
                            file_name=f"bds_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )

            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.header("ℹ️ Thông tin")
    
    st.markdown("**Model:**")
    st.info("🔹 Trích xuất: `bds-pro`")
    
    st.markdown("---")
    
    st.markdown("**Trích xuất:**")
    items = [
        "Địa chỉ",
        "Giá, Diện tích",
        "Phòng ngủ, WC",
        "Hướng nhà",
        "Pháp lý",
        "Tiện ích"
    ]
    for item in items:
        st.markdown(f"• {item}")
    
    st.markdown("---")
    st.caption("**Powered by:** Ollama AI")

# =========================
# Footer
# =========================
st.markdown("---")
with st.expander("ℹ️ Hướng dẫn"):
    st.markdown("""
    ### 📥 Cách sử dụng:
    1. Nhập/dán nội dung bài đăng vào ô bên trái
    2. Nhấn "Trích xuất thông tin"
    3. Xem kết quả và tải xuống Excel/JSON
    
    ### 🔄 Luồng:
    - **Text → bds-pro → JSON**
    
    ### 📋 Yêu cầu:
    - Ollama đang chạy
    - Model `bds-pro` đã được cài đặt
    - Chạy lệnh: `ollama create bds-pro -f Modelfile`
    """)

st.caption("📥 Powered by Ollama AI • Trích xuất thông tin tự động")
