from django.shortcuts import render
import random
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from kavenegar import KavenegarAPI, APIException

from .models import User, Device, UserProfile

KAVENEGAR_API_KEY = 'YOUR_KAVENEGAR_API_KEY'  # اینجا کلید خودت رو بذار

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'message': 'phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            user = User.objects.create_user(phone_number=phone_number)
            UserProfile.objects.create(user=user)
            Device.objects.create(user=user)

        code = random.randint(100000, 999999)
        cache.set(str(phone_number), code, 300)

        # ارسال پیامک با کاوه نگار
        try:
            api = KavenegarAPI('4255446542394350642F466D5A74536C4E5866616F50742F514544424E4F77782B34366F686261346A4A673D')
            params = {
                'sender': '2000660110',
                'receptor': phone_number,
                'message': f'کد تایید شما: {code}'
            }
            result = api.sms_send(params)
            print(result)

        except APIException as e:
             print(f"Kavenegar API error: {e}")
             return Response({'message': f'خطا در ارسال پیامک: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        profile = None
        if hasattr(user, 'userprofile'):
            profile = user.userprofile

        user_data = {
            'full_name': user.get_full_name() or '',
            'phone_number': user.phone_number,
            'email': user.email or '',
            'avatar': profile.avatar.url if profile and profile.avatar else '',
        }

        return Response({'message': 'کد تایید ارسال شد', 'user': user_data})

@method_decorator(csrf_exempt, name='dispatch')
class GetTokenView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        cached_code = cache.get(str(phone_number))
        if not cached_code or str(code) != str(cached_code):
            return Response({'message': 'کد نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(str(phone_number))

        refresh = RefreshToken.for_user(user)

        profile = None
        if hasattr(user, 'userprofile'):
            profile = user.userprofile

        user_data = {
            'full_name': user.get_full_name() or '',
            'phone_number': user.phone_number,
            'email': user.email or '',
            'avatar': profile.avatar.url if profile and profile.avatar else '',
        }

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data
        })

def phone_auth_view(request):
    return render(request, 'users/phone_auth.html')
