#!/usr/bin/env python3
"""Clone giọng và đọc văn bản tiếng Việt bằng OmniVoice (k2-fsa/OmniVoice).
Ví dụ:
  python clone.py --ref mau.wav --ref-text "Lời đúng trong mẫu" --text "Xin chào các bạn" --out ra.wav
  python clone.py --ref mau.wav --ref-text @mau.txt --text-file kichban.txt --out ra.wav
  python clone.py --save-prompt giong.prompt --ref mau.wav --ref-text @mau.txt     # lưu giọng để dùng lại, khỏi phân tích mẫu mỗi lần
  python clone.py --prompt giong.prompt --text "Đọc bằng giọng đã lưu" --out ra.wav
Mẫu giọng (ref): 5–30 giây, ít tạp âm, nói rõ; ref-text phải khớp ĐÚNG lời trong mẫu."""
import argparse, time, torch, soundfile as sf
from omnivoice import OmniVoice

def txt(v):
    if v and v.startswith("@"): return open(v[1:], encoding="utf-8").read().strip()
    return v

ap = argparse.ArgumentParser()
ap.add_argument("--ref"); ap.add_argument("--ref-text"); ap.add_argument("--prompt"); ap.add_argument("--save-prompt")
ap.add_argument("--text"); ap.add_argument("--text-file"); ap.add_argument("--out", default="ra.wav")
ap.add_argument("--device", default="auto", choices=["auto", "mps", "cpu"])
a = ap.parse_args()
dev = "mps" if a.device == "auto" and torch.backends.mps.is_available() else ("cpu" if a.device == "auto" else a.device)
t0 = time.time()
# Nạp ở CPU rồi mới chuyển sang MPS: nạp thẳng device_map="mps" có thể bị segfault trên Mac.
m = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float16)
if dev == "mps": m = m.to("mps")
print(f"đã nạp model ({dev}) {time.time()-t0:.0f}s", flush=True)

if a.save_prompt:
    if not (a.ref and a.ref_text): raise SystemExit("Cần --ref và --ref-text để lưu giọng")
    m.create_voice_clone_prompt(ref_audio=a.ref, ref_text=txt(a.ref_text)).save(a.save_prompt); print("đã lưu giọng:", a.save_prompt)
    if not (a.text or a.text_file): raise SystemExit(0)

text = a.text or (open(a.text_file, encoding="utf-8").read().strip() if a.text_file else None)
if not text: raise SystemExit("Cần --text hoặc --text-file")
t0 = time.time()
if a.prompt:
    from omnivoice import VoiceClonePrompt
    audio = m.generate(text=text, voice_clone_prompt=VoiceClonePrompt.load(a.prompt))
else:
    audio = m.generate(text=text, ref_audio=a.ref, ref_text=txt(a.ref_text)) if a.ref else m.generate(text=text)
wav = audio[0].squeeze(); sf.write(a.out, wav, 24000)
print(f"xong {a.out}: {len(wav)/24000:.1f}s âm thanh, tạo mất {time.time()-t0:.0f}s")
