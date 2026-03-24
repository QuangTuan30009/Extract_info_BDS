=============================================================================================
TRÍCH XUẤT THÔNG TIN BẤT ĐỘNG SẢN TỪ VĂN BẢN
=============================================================================================

GIỚI THIỆU

Ứng dụng AI tự động trích xuất thông tin bất động sản từ văn bản sang định dạng JSON.

TÍNH NĂNG:
- Trích xuất thông tin BDS từ văn bản (địa chỉ, giá, diện tích, phòng ngủ, WC, v.v.)
- Xuất kết quả sang Excel hoặc JSON
- Sử dụng model Qwen 2.5 7B qua Ollama

=============================================================================================
CÀI ĐẶT
=============================================================================================

BƯỚC 1: YÊU CẦU HỆ THỐNG

- Python 3.9+
- Ollama (tải tại: https://ollama.com)
- RAM: Tối thiểu 8GB

BƯỚC 2: CÀI ĐẶT OLLAMA VÀ BASE MODEL

Tải Ollama từ: https://ollama.com/download

Tải base model:
ollama pull qwen2.5:7b

Kiểm tra:
ollama list

BƯỚC 3: TẠO CUSTOM MODEL TRÍCH XUẤT

Tạo model trích xuất:
ollama create bds-pro -f Modelfile

Kiểm tra:
ollama list

BƯỚC 4: CÀI ĐẶT THƯ VIỆN PYTHON

pip install -r requirements.txt

Hoặc cài thủ công:
pip install streamlit ollama pandas openpyxl numpy

=============================================================================================
CHẠY ỨNG DỤNG
=============================================================================================

streamlit run app.py

Ứng dụng sẽ mở tại: http://localhost:8501

=============================================================================================
CÁCH SỬ DỤNG
=============================================================================================

1. Nhập/dán nội dung bài đăng BDS vào ô bên trái
2. Nhấn nút "Trích xuất thông tin"
3. Xem kết quả và tải xuống Excel hoặc JSON

THÔNG TIN TRÍCH XUẤT:
- Địa chỉ (số nhà, đường, phường, quận)
- Giá, Diện tích
- Phòng ngủ, WC, Số tầng
- Hướng nhà, Hướng ban công
- Pháp lý (sổ hồng, sổ đỏ...)
- Tiện ích xung quanh
- Số điện thoại

=============================================================================================
GHI CHÚ
=============================================================================================

- Model sử dụng: bds-pro (dựa trên Qwen 2.5 7B)
- Temperature = 0 (kết quả ổn định, chính xác)
- Chỉ trích xuất thông tin có trong văn bản, không đoán hay suy luận

=============================================================================================
LỖI THƯỜNG GẶP
=============================================================================================

1. "Connection refused":
   - Kiểm tra Ollama đang chạy: ollama list
   - Khởi động lại: ollama serve

2. "Model not found":
   - Chạy lại: ollama create bds-pro -f Modelfile

3. "Out of memory":
   - Đóng các ứng dụng khác
   - Cần RAM tối thiểu 8GB

=============================================================================================
HỖ TRỢ
=============================================================================================

Powered by: Ollama AI + Streamlit
