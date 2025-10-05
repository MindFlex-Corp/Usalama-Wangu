import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Alerts.models import Alert
from Alerts.models import SMS
from Zones.models import Zone
from .serializers import AlertSerializer, SMSSerializer, ZoneSerializer
from rest_framework import generics


# Create your views here.
class AlertListCreateView(APIView):
    def get(self, request):
        alerts = Alert.objects.all().order_by('-created_at')[:50]
        serializer = AlertSerializer(alerts, many=True)
        return Response({"alerts": serializer.data})

    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        address = request.data.get('address')
        accuracy = request.data.get('accuracy')
        audio_file = request.FILES.get('audio')

        if not audio_file:
            return Response({'message': 'Audio file is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not latitude or not longitude:
            return Response({'message': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Upload to Cloudinary
        try:
            upload_response = cloudinary.uploader.upload(
                audio_file,
                folder="Usalama_wangu_emergency_audio",
                resource_type="video"
            )
            audio_url = upload_response["secure_url"]
        except Exception as e:
            return Response({'error': f'Cloudinary upload failed: {e}'}, status=500)

        # Create Alert
        alert = Alert.objects.create(
            latitude=float(latitude),
            longitude=float(longitude),
            address=address,
            accuracy=float(accuracy) if accuracy else None,
            audio_url=audio_url,
            notified_contacts=[],
            delivered_to_authorities=False
        )

        serializer = AlertSerializer(alert)
        return Response(
            {
                "success": True,
                "alert": serializer.data,
                "message": "Emergency alert created and notifications sent"
            },
            status=status.HTTP_201_CREATED
        )


class AlertSMSHistoryView(APIView):
    def get(self, request, alert_id):
        sms_records = SMS.objects.filter(alert_id=alert_id)
        serializer = SMSSerializer(sms_records, many=True)
        return Response({"sms_records": serializer.data})


class ZoneList(generics.ListCreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class ZoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
