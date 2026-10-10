"""Bot profil rasmini yaratadi: logo.png (640x640)."""
from PIL import Image, ImageDraw, ImageFont

SIZE = 640
img = Image.new("RGB", (SIZE, SIZE))
px = img.load()
# Diagonal gradient: ko'k -> moviy
c1, c2 = (18, 70, 160), (0, 160, 190)
for y in range(SIZE):
    for x in range(SIZE):
        t = (x + y) / (2 * SIZE)
        px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 230, index=1)  # Bold
except Exception:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 230)

letters = [("Ö", 0, 0), ("Ğ", 1, 0), ("Ş", 0, 1), ("Ç", 1, 1)]
cell = SIZE // 2
for ch, cx, cy in letters:
    bbox = d.textbbox((0, 0), ch, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = cx * cell + (cell - w) // 2 - bbox[0]
    y = cy * cell + (cell - h) // 2 - bbox[1] + (10 if cy == 0 else -10)
    d.text((x + 6, y + 6), ch, font=font, fill=(10, 45, 110))
    d.text((x, y), ch, font=font, fill="white")

img.save("logo.png")
print("logo.png saved")
