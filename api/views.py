import jwt
import datetime
from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProductSerializer
from django.http import JsonResponse, HttpResponse
from .models import User, Product
from rest_framework.parsers import MultiPartParser,FormParser
import tensorflow as tf
from io import BytesIO
from PIL import Image
import numpy as np
from django.conf import settings
# img_size = 128
img_size = 120 #for anup.h5

# generator = tf.keras.models.load_model('milanmodel.keras', custom_objects={'generator_loss':generator_loss})
# custom_objects={'generator_loss':generator_loss},compile = False,


# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response =  Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt' : token
        }
        
        return response
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

        # return Response(token)
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response
    



#yaha dekhi chai ishan le change gareko hai . yesma chai load garna ra color ko lagi euta api banako arko chai colored version retrieve garna arko api banako     
class ImageView(APIView):
    def colorize(self, image):

        generator = tf.keras.models.load_model('anup.h5',compile=False)
        a = []

        # Resize the RGB image
        rgb = image.resize((img_size, img_size))

        # Convert to grayscale
        gray = rgb.convert('L')

        # Convert to numpy array, normalize, and reshape grayscale array
        gray_array = np.asarray(gray).reshape(( img_size, img_size, 1)) / 255.0
        a.append(gray_array)
        d= np.asanyarray(a)
        

        # Generate colorized output
        output = generator(d[0:]).numpy()

        # Convert output to image format
        color_output = Image.fromarray((output[0] * 255).astype('uint8')).resize((1024, 1024))

        return color_output

    def post(self, request):
        if request.FILES.get('image'):
            uploaded_image = request.FILES['image']
            uploaded_image_instance = Product(image=uploaded_image)
            uploaded_image_instance.save()

            id = request.POST.get('user_id')
            print("hellow ajkdljfdjfjd")
            id_instance = Product(user_id = id)
            id_instance.save()

            # Get the uploaded image instance
            image_instance = uploaded_image_instance.image

            # Open the image using PIL
            image = Image.open(uploaded_image)

            # Colorize the image
            colorized_image = self.colorize(image)

            # Save the colorized image
            colorized_image_io = BytesIO()
            colorized_image.save(colorized_image_io, format='JPEG')
            colorized_image_io.seek(0)

            # Update the image field with the colorized image
            uploaded_image_instance.colorized_image.save('colorized_' + image_instance.name, colorized_image_io)
            uploaded_image_instance.save()

            # Get the URL of the colorized image
            
            colorized_image_url = uploaded_image_instance.colorized_image.url
            image_url = request.build_absolute_uri(colorized_image_url)

            # Serialize the product instance
            serialized_product = ProductSerializer(uploaded_image_instance).data

            return JsonResponse({'colorized_image_url': image_url, 'product': serialized_product})

        return JsonResponse({'error': 'No image provided'}, status=400)
    
class ColorizedImageView(APIView):
    def get(self, request):
        try:
            # Retrieve the last Product object with a colorized image
            product = Product.objects.exclude(colorized_image__isnull=True).exclude(colorized_image='').order_by('-id').first()
            if product:
                # As colorized_image is an ImageField
                colorized_image_url = product.colorized_image.url
                return Response({'colorized_image_url': colorized_image_url})
            else:
                return Response({'error': 'No colorized image found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class AllImageView(APIView):
    # def get(self, request):
    #     try:
    #         # Retrieve all Product objects with colorized images
    #         products = Product.objects.exclude(colorized_image__isnull=True).exclude(colorized_image='')

    #         # Serialize the products
    #         serialized_products = ProductSerializer(products, many=True).data

    #         return Response({'colorized_images': serialized_products})
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=500)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve colorized images associated with the currently logged-in user
            products = Product.objects.filter(user=request.user).exclude(colorized_image__isnull=True).exclude(colorized_image='')

            serialized_products = ProductSerializer(products, many=True).data

            return Response({'colorized_images': serialized_products})
        except Exception as e:
            return Response({'error': str(e)}, status=500)