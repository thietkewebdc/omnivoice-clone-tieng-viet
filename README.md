# OmniVoice — clone giọng tiếng Việt trên máy (Thiết Kế Web DC)

Công cụ nhỏ dùng **[OmniVoice](https://github.com/k2-fsa/OmniVoice)** (k2-fsa, giấy phép Apache-2.0) để **clone giọng** từ một đoạn mẫu 5–30 giây rồi đọc văn bản tiếng Việt. Chạy hoàn toàn trên máy bạn. Dùng trong bộ skill video hướng dẫn của Bùi Viết Cường (Thiết Kế Web DC).

> OmniVoice là dự án của k2-fsa; repo này chỉ là script gọi và ghi chú kinh nghiệm chạy thực tế. Model tự tải về lần chạy đầu.

## Cài đặt
```bash
python3.11 -m venv .venv && source .venv/bin/activate     # đã chạy ổn với Python 3.11
pip install omnivoice soundfile
```

## Dùng
```bash
# 1) Clone + đọc
python clone.py --ref mau.wav --ref-text "Lời đúng trong mẫu" --text "Xin chào các bạn" --out ra.wav
# 2) Lưu giọng để dùng lại (nhanh hơn)
python clone.py --save-prompt giong.prompt --ref mau.wav --ref-text @mau.txt
python clone.py --prompt giong.prompt --text-file kichban.txt --out ra.wav
```

## Kinh nghiệm chạy thực tế (Mac Apple Silicon, 8GB)
- Phải **nạp model ở CPU rồi `.to("mps")`**; nạp thẳng `device_map="mps"` bị segfault (script đã làm sẵn).
- Tốc độ: khoảng **3 lần** thời lượng âm thanh. Chất lượng clone tiếng Việt tốt hơn VieNeu-TTS nhưng chậm hơn; cần nhanh thì dùng [VieNeu-TTS](https://github.com/thietkewebdc/VieNeu-TTS).
- Mẫu giọng càng sạch (không nhạc, không ồn) thì giọng clone càng giống. `ref-text` sai lời → giọng méo.

## Đạo đức và pháp lý
**Chỉ clone giọng của chính bạn, hoặc giọng của người đã đồng ý rõ ràng.** Không dùng để mạo danh. Repo không kèm mẫu giọng nào.

## Giấy phép
Script trong repo: dùng tự do, giữ ghi công "Thiết Kế Web DC · Bùi Viết Cường". OmniVoice theo giấy phép Apache-2.0 của k2-fsa.
