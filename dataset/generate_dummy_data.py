import os
import cv2
import numpy as np

# Soil classes and their base colors (BGR format roughly approximating soil colors)
classes = {
    'Clay': (60, 80, 150),
    'Loam': (40, 60, 110),
    'Sandy': (130, 180, 210),
    'Loamy Sand': (100, 140, 180),
    'Sandy Loam': (80, 110, 160)
}

base_dir = '/Users/kovidchhabra/Desktop/antigravity project/dataset/train'
os.makedirs(base_dir, exist_ok=True)

# Generate 50 images per class for dummy training
num_images = 50
img_size = (224, 224, 3)

for class_name, color in classes.items():
    class_dir = os.path.join(base_dir, class_name)
    os.makedirs(class_dir, exist_ok=True)
    
    for i in range(num_images):
        # Create base image with the soil color
        img = np.full(img_size, color, dtype=np.uint8)
        
        # Add random noise to simulate texture
        noise = np.random.randint(-30, 30, img_size, dtype=np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Add some random lines or blobs for more texture variation
        for _ in range(5):
            x1, y1 = np.random.randint(0, 224, 2)
            x2, y2 = np.random.randint(0, 224, 2)
            thickness = np.random.randint(1, 5)
            cv2.line(img, (x1, y1), (x2, y2), (max(0, color[0]-20), max(0, color[1]-20), max(0, color[2]-20)), thickness)
            
        cv2.imwrite(os.path.join(class_dir, f'dummy_{i}.jpg'), img)

print("Dummy dataset generated successfully!")
