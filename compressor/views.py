from django.shortcuts import render










from django.shortcuts import render
from .models import ImageUpload
from .utils import compress_image



from django.shortcuts import render
from .models import ImageUpload
from .utils import process_image

def index(request):
    return render(request, 'index.html')

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        original_image = request.FILES['image']
        optimized_image = process_image(original_image)

        image_upload = ImageUpload(
            image=original_image,
            optimized_image=optimized_image,
            original_size=original_image.size,
            optimized_size=optimized_image.size
        )
        image_upload.save()
        return render(request, 'compressor/upload_success.html', {'image': image_upload})

    return render(request, 'compressor/upload_image.html')





