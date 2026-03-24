# Extract_info_BDS

Ứng dụng AI trích xuất thông tin bất động sản từ văn bản và xuất kết quả dạng JSON/Excel.

## Tính năng

- Trích xuất thông tin BĐS: địa chỉ, giá, diện tích, phòng ngủ, WC, số tầng...
- Trả kết quả có cấu trúc để dùng tiếp cho phân tích/lưu trữ.
- Xuất file JSON hoặc Excel.
- Chạy qua giao diện web với Streamlit.

## Yêu cầu

- Python 3.9+
- Ollama (https://ollama.com)
- RAM đề xuất: tối thiểu 8GB

## Cài đặt

1. Cài Ollama và tải model nền:

	 ```bash
	 ollama pull qwen2.5:7b
	 ```

2. Tạo model tùy biến từ file `Modelfile`:

	 ```bash
	 ollama create bds-pro -f Modelfile
	 ```

3. Cài thư viện Python:

	 ```bash
	 pip install -r requirements.txt
	 ```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Mở trình duyệt tại: `http://localhost:8501`

## Cách dùng

1. Dán nội dung bài đăng BĐS vào ô nhập liệu.
2. Nhấn nút trích xuất thông tin.
3. Kiểm tra kết quả và tải về JSON/Excel nếu cần.

## Lỗi thường gặp

- `Connection refused`:
	- Kiểm tra Ollama đang chạy.
	- Thử chạy lại: `ollama serve`
- `Model not found`:
	- Tạo lại model: `ollama create bds-pro -f Modelfile`
- Thiếu RAM:
	- Đóng ứng dụng nặng khác, đảm bảo máy có đủ bộ nhớ.

## Ghi chú

- Model chính: `bds-pro` (dựa trên Qwen 2.5 7B).
- Thiết lập temperature thấp để ưu tiên kết quả ổn định.