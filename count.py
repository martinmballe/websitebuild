import torch
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms
from models import vgg19

def save_density_map(density_map, output_path):
    try:
        density_map = density_map / np.max(density_map) * 255.0
        density_map = density_map.astype(np.uint8)
        density_map = cv2.applyColorMap(density_map, cv2.COLORMAP_JET)
        cv2.imwrite(output_path, density_map)
        print(f"Density map saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving density map: {e}")
        return False

def process_image(image_path, model_path, output_path=''):
    try:
        device = torch.device('cpu')  # use 'cuda' for GPU

        # Load the model
        model = vgg19()
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.to(device).eval()

        # Load and transform the image
        image = Image.open(image_path).convert('RGB')
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = transform(image).unsqueeze(0).to(device)

        # Perform inference
        with torch.no_grad():
            outputs = model(image_tensor)
            density_map = outputs[0].cpu().numpy().squeeze()

        # Calculate the estimated count
        estimated_count = np.sum(density_map)

        # Optionally save the density map
        if output_path:
            if not save_density_map(density_map, output_path):
                raise Exception("Failed to save density map")

        return estimated_count, output_path
    except Exception as e:
        print(f"Error processing image: {e}")
        return -1, None  # Returning -1 or any appropriate error indicator
if __name__ == '__main__':
    model_path = 'pretrained_models/best_model_7.pth'
    image_path = 'haps/example.jpg'  # Make sure to specify a valid image file
    output_path = 'static/density_example.jpg'  # Ensure this path is correct
    count, _ = process_image(image_path, model_path, output_path)
    print(f"Estimated count: {count}")