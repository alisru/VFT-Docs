import base64

with open('psochic_hegemony_compass.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')

with open('image_data.js', 'w', encoding='utf-8') as f:
    f.write('window.COMPASS_B64 = "data:image/png;base64,' + b64 + '";\n')

print("image_data.js written successfully, size:", len(b64))
