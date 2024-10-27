from PIL import Image, ImageEnhance
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import torch
from torchvision import transforms
import numpy as np
import cv2

def compress_image(image):
    im = Image.open(image)
    im_io = io.BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = InMemoryUploadedFile(
        im_io, 'ImageField', image.name, 'image/jpeg', im_io.getbuffer().nbytes, None
    )
    return new_image

def load_esrgan_model():
    try:
        model = torch.hub.load('xinntao/ESRGAN', 'esrgan')
        model.eval()
        return model
    except Exception as e:
        print(f"Error loading ESRGAN model: {e}")
        return None

def enhance_image_quality(image):
    model = load_esrgan_model()
    if model is None:
        return image  

   
    img_np = np.array(image)
    img_denoised = cv2.fastNlMeansDenoisingColored(img_np, None, 10, 10, 7, 21)

   
    img_denoised_pil = Image.fromarray(img_denoised)


    enhancer = ImageEnhance.Contrast(img_denoised_pil)
    img_enhanced = enhancer.enhance(1.5) 

    
    preprocess = transforms.ToTensor()
    img_tensor = preprocess(img_enhanced).unsqueeze(0)

    with torch.no_grad():
        sr_image = model(img_tensor)

    sr_image = sr_image.squeeze().permute(1, 2, 0).cpu().numpy()
    sr_image = (sr_image * 255).astype(np.uint8)
    sr_image_pil = Image.fromarray(sr_image)

    return sr_image_pil

def process_image(image):
    compressed_image = compress_image(image)
    enhanced_image = enhance_image_quality(Image.open(compressed_image))
    
    enhanced_io = io.BytesIO()
    enhanced_image.save(enhanced_io, 'JPEG', quality=95)
    new_enhanced_image = InMemoryUploadedFile(
        enhanced_io, 'ImageField', image.name, 'image/jpeg', enhanced_io.getbuffer().nbytes, None
    )
    return new_enhanced_image
