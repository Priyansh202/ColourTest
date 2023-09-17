from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from sklearn.cluster import KMeans
from .serializers import UrineStripSerializer
import cv2
import numpy as np

class ProcessUrineStrip(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = UrineStripSerializer(data=request.data)

        if serializer.is_valid():
            try:
                uploaded_image = request.FILES['image']
                image_data = uploaded_image.read()

                image = cv2.imdecode(np.fromstring(image_data, np.uint8), cv2.IMREAD_COLOR)
                color_info = self.extract_colors(image)

               
                self.save_color_info(color_info)

                return Response({'color_info': color_info})

            except Exception as e:
                return Response({'error': str(e)}, status=400)

        return Response(serializer.errors, status=400)

    """def extract_colors(self, image):
        # Implement your color extraction logic here
        # This is just a placeholder example
        # Replace this with your actual logic

        # For demonstration purposes, we'll extract colors in BGR format
        # You may need to convert BGR to RGB as per your requirement
        colors = []

        for row in image:
            for pixel in row:
                b, g, r = pixel
                colors.append({'r': r, 'g': g, 'b': b})

        return colors"""
    def extract_colors(self, image):
        
        num_colors = 5 
        pixels = image.reshape(-1, 3)

        
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)

       
        colors = kmeans.cluster_centers_.astype(int)

      
        colors = [color[::-1] for color in colors]

        return [{'r': r, 'g': g, 'b': b} for (r, g, b) in colors]


    def save_color_info(self, color_info):
     
        pass

def home(request):
    return render(request,'app/index.html')