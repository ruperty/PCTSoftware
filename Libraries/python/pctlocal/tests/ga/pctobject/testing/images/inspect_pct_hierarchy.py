from PIL import Image, ImageDraw, ImageStat
import os

path = 'pct_hierarchy_control.png'
if not os.path.exists(path):
    print('MISSING:', path)
    raise SystemExit(1)

img = Image.open(path).convert('RGB')
w,h = img.size
print('size:', w, h)

# convert to grayscale and find non-white bbox
gray = img.convert('L')
# threshold to consider 'content' (not white)
th = 250
mask = gray.point(lambda p: 255 if p < th else 0)
bbox = mask.getbbox()
print('bbox:', bbox)

# compute fraction of white pixels per column
cols = []
px = list(gray.getdata())
for x in range(w):
    col_white = 0
    for y in range(h):
        if px[y*w + x] >= th:
            col_white += 1
    cols.append(col_white / h)

# fraction of columns that are > 95% white
mostly_white_cols = sum(1 for v in cols if v > 0.95)
print('mostly white columns:', mostly_white_cols, 'of', w, f'({mostly_white_cols/w:.2%})')

# leftmost and rightmost content columns
left = next((i for i,v in enumerate(cols) if v < 0.95), None)
right = next((i for i,v in reversed(list(enumerate(cols))) if v < 0.95), None)
print('leftmost content column:', left, 'rightmost:', right)

# percentage whitespace on left and right halves
half = w//2
left_whitespace = sum(1 for v in cols[:half] if v > 0.95)/half
right_whitespace = sum(1 for v in cols[half:] if v > 0.95)/(w-half)
print('left half white % of columns:', f'{left_whitespace:.2%}', 'right half:', f'{right_whitespace:.2%}')

# draw bbox on copy and save
dbg = img.copy()
d = ImageDraw.Draw(dbg)
if bbox:
    d.rectangle(bbox, outline='red', width=5)
dbg.save('pct_hierarchy_control_debug.png')
print('wrote debug image: pct_hierarchy_control_debug.png')
