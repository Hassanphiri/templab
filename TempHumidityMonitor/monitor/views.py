from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Reading
import json
import logging



def index(request):
    try:
        # Try to fetch the latest reading
        latest_reading = Reading.objects.latest('timestamp')
    except Reading.DoesNotExist:
        # Handle the case where no readings are in the database
        latest_reading = None

    # Pass the latest reading to the template
    return render(request, 'monitor/index.html', {'latest_reading': latest_reading})
    
    


logger = logging.getLogger(__name__)

@csrf_exempt
def api_readings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            # Log the data being received
            logger.info(f"Received data: Temperature={temperature}, Humidity={humidity}")

            if temperature is not None and humidity is not None:
                Reading.objects.create(temperature=temperature, humidity=humidity, timestamp=timezone.now())
                logger.info("New reading saved to the database.")
                return JsonResponse({"status": "success", "message": "Data received"})
            else:
                return JsonResponse({"status": "fail", "message": "Invalid data"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": "fail", "message": "Invalid JSON format"}, status=400)
    elif request.method == 'GET':
        try:
            latest_reading = Reading.objects.latest('timestamp')
            local_time = timezone.localtime(latest_reading.timestamp)
            data = {
                'temperature': latest_reading.temperature,
                'humidity': latest_reading.humidity,
                'timestamp': local_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return JsonResponse(data)
        except Reading.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "No readings found"}, status=404)
    else:
        return JsonResponse({"status": "fail", "message": "Invalid request method"}, status=405)

def historical_readings(request):
    # Get all readings or filter by some criteria (e.g., last 7 days)
    readings = Reading.objects.all().order_by('-timestamp')[:100]  # Last 100 records, adjust as needed
    
    data = [
        {
            'temperature': reading.temperature,
            'humidity': reading.humidity,
            'timestamp': reading.timestamp
        }
        for reading in readings
    ]
    
    return JsonResponse(data, safe=False)
