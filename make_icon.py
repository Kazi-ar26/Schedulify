from PIL import Image

image = Image.open("Assets/icons/schedulify_icon.png")

image.save(
    "Assets/icons/schedulify.ico",
    format="ICO",
    sizes=[
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ],
)

print("Icon created successfully.")