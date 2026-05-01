from PIL import Image

def process_image(input_path, output_path):
    # Open the image and convert to RGBA
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    # Navy blue for the text/icon to replace white
    navy_r, navy_g, navy_b = 0, 58, 112

    for item in datas:
        r, g, b, a = item
        # If it's dark (close to black background), make it transparent
        # We use a threshold of 45 to catch compression artifacts
        if r < 45 and g < 45 and b < 45:
            new_data.append((0, 0, 0, 0))
        # If it's very bright (close to white text/icon), turn to navy
        elif r > 200 and g > 200 and b > 200:
            # We preserve the original alpha just in case, but usually it's 255
            new_data.append((navy_r, navy_g, navy_b, a))
        else:
            # Leave colors (red/green rings) as they are
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

input_image = r"C:\Users\LENOVO\.gemini\antigravity\brain\1225200d-5d2a-4db1-b47b-35d0903f8bb9\media__1777651488989.png"
output_image = r"C:\Users\LENOVO\.gemini\antigravity\scratch\Odm-Laboratories\logo.png"

process_image(input_image, output_image)
print("Logo processed successfully.")
