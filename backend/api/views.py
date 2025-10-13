import cloudinary.uploader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Alerts.models import Alert
from Alerts.models import SMS
from Zones.models import Zone
from .serializers import AlertSerializer, SMSSerializer, ZoneSerializer
from rest_framework import generics
from django.core.mail import send_mail, EmailMessage
from dotenv import load_dotenv
import os
from .audio_handler import upload_audio

load_dotenv()


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

        # Upload audio to both Cloudinary and Azure
        azure_url, cloudinary_url = upload_audio(audio_file)

        # Send email to emergency contacts
        contacts = request.data.getlist('notified_contacts')
        if contacts:
            subject = "A registered user is in immediate danger!"
            message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background-color: #f7f9fb;
                    color: #222;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .container {{
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 25px;
                    max-width: 600px;
                    margin: auto;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #c62828;
                    text-align: center;
                }}
                p {{
                    margin: 10px 0;
                }}
                a {{
                    color: #1565c0;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .alert {{
                    background-color: #fff3cd;
                    border-left: 5px solid #ff9800;
                    padding: 10px 15px;
                    border-radius: 5px;
                    color: #856404;
                    margin-top: 20px;
                    font-weight: 500;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 0.9em;
                    text-align: center;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🚨 Emergency Alert — Immediate Action Required</h2>
                <p><strong>📍 Location:</strong> {address or "Unknown address"}</p>
                <p><strong>🌍 Coordinates:</strong> Latitude: {latitude}, Longitude: {longitude}</p>
                <p><strong>🗺️ Google Maps:</strong>
                    <a href="https://maps.google.com/?q={latitude},{longitude}" target="_blank">
                        View on Google Maps
                    </a>
                </p>
                <p><strong>🎤 Audio Recording:</strong>
                    <a href="{cloudinary_url}" target="_blank">Listen to the audio</a>
                    <a href="{azure_url}" target="_blank">Download the audio</a>
                </p>
            
                <div class="alert">
                    ⚠️ Please take immediate action — contact the person and notify emergency services. You will be receiving the
                    user's location every 5 minutes for the next one hour.
                </div>
            
                <p class="footer">
                    This alert was generated automatically by <strong>Usalama Wangu</strong> for user safety.
                </p>
            </div>
        </body>
        </html>
        """

            from_email = os.getenv("EMAIL_HOST_USER")
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=contacts,
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

        # Create Alert
        alert = Alert.objects.create(
            latitude=float(latitude),
            longitude=float(longitude),
            address=address,
            accuracy=float(accuracy) if accuracy else None,
            audio_url=cloudinary_url,
            notified_contacts=[contacts],
            delivered_to_authorities=False
        )

        serializer = AlertSerializer(alert)
        return Response(
            {
                "success": True,
                "alert": serializer.data,
                "message": "Emergency alert created and notifications sent",
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
