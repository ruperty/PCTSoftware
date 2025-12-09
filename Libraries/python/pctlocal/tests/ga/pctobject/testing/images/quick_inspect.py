from PIL import Image
img=Image.open('pct_hierarchy_control_v2.png').convert('L')
w,h=img.size
print('size',w,h)
th=250
mask=img.point(lambda p:255 if p < th else 0)
print('bbox', mask.getbbox())
