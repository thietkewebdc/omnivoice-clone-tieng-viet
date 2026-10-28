import time, torch, soundfile as sf
from omnivoice import OmniVoice
t=time.time()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float16)
model = model.to("mps")
print("load", round(time.time()-t,1), flush=True)
text = "Xin chào các bạn, hôm nay mình sẽ giải thích cho bạn hiểu thiết kế website chuẩn SEO là gì."
t=time.time()
audio = model.generate(text=text)
print("gen", round(time.time()-t,1), flush=True)
sf.write("kiem_tra.wav", audio[0].squeeze(), 24000)
