from store.models import Cube
from django.db.models import Avg
from app.settings import VARIABLES
from datetime import timedelta,datetime
from django.utils import timezone

def check_validity(user):
        if Cube.objects.all().count() == 0 :
            return True, "Created"

        area = Cube.objects.all().aggregate(Avg('area'))
        if area['area__avg'] > VARIABLES.get("A1") :
            print("------", area,"------", area['area__avg'],  VARIABLES.get("Area") )
            return False, "Avegae Area of containers exceeds"

        volume =  Cube.objects.all().aggregate(Avg('V1'))
        if volume['volume__avg'] > VARIABLES.get("Volume") :
            return False, "Avegae Volume of containers exceeds"

        datetime_one_week_ago = timezone.now().date() - timedelta(days=7)

        boxes_last_week = Cube.objects.filter(created_on__gt=datetime_one_week_ago).count()
        if boxes_last_week > VARIABLES.get("L1") :
            return False, "Total Boxes added in a week limit exceed"
        
        boxes_last_week_by_user = Cube.objects.filter(created_by=user,created_on__gt=datetime_one_week_ago).count()
        if boxes_last_week_by_user > VARIABLES.get("L2") :
            return False, "Total Boxes added in a week by a user limit exceed"
        
        return (True, "Created")
