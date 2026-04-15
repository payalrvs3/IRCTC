from django.core.management.base import BaseCommand
from services.models import CateringVendor, MenuItem, TourPackage
from trains.models import Station

class Command(BaseCommand):
    help = "Seeds catering and tour data"

    def handle(self, *args, **kwargs):
        vendors_data = [
            ("CSTM","Bombay Tiffin House","North Indian",4.3,100,25),
            ("CSTM","Quick Bites Cafe","Fast Food",4.1,80,20),
            ("NDLS","Delhi Darbar","Mughlai",4.5,120,30),
            ("NDLS","The Chai Wala","Beverages",4.4,60,15),
            ("HWH","Bengali Rasoi","Bengali",4.2,100,25),
            ("MAS","South Spice","South Indian",4.6,100,20),
        ]
        for code,name,cuisine,rating,min_order,delivery in vendors_data:
            try:
                st = Station.objects.get(code=code)
                CateringVendor.objects.get_or_create(name=name,station=st,
                    defaults={"cuisine_type":cuisine,"rating":rating,"min_order":min_order,"delivery_time_minutes":delivery})
            except Station.DoesNotExist:
                pass

        menu_items = [
            ("Veg Thali","Full veg meal","MEAL",120,True,"🍱"),
            ("Rajma Chawal","Rajma with rice","MEAL",90,True,"🍛"),
            ("Chicken Biryani","Aromatic biryani","MEAL",160,False,"🍚"),
            ("Veg Sandwich","Grilled sandwich","SNACK",60,True,"🥪"),
            ("Samosa (2 pcs)","Crispy samosas","SNACK",30,True,"🥟"),
            ("Masala Chai","Spiced tea","BEVERAGE",20,True,"☕"),
            ("Cold Coffee","Chilled coffee","BEVERAGE",60,True,"🧊"),
            ("Poha Breakfast","Poha with peanuts","BREAKFAST",50,True,"🌾"),
            ("Gulab Jamun","Sweet milk dumplings","DESSERT",40,True,"🍮"),
            ("Combo Meal","Thali + drink + dessert","COMBO",180,True,"🎁"),
        ]
        for vendor in CateringVendor.objects.all():
            for name,desc,cat,price,is_veg,emoji in menu_items:
                MenuItem.objects.get_or_create(vendor=vendor,name=name,
                    defaults={"description":desc,"category":cat,"price":price,"is_veg":is_veg,"image_emoji":emoji})

        tours = [
            ("Golden Triangle Tour","HERITAGE","Delhi to Agra to Jaipur",5,6,12999,16999,"Rail+hotel+breakfast","Delhi","Jaipur","🕌","Taj Mahal, Red Fort, Amber Fort"),
            ("Kashmir on Rails","HILL_STATION","Delhi to Srinagar",7,8,18500,24000,"Train+houseboat+meals","Delhi","Srinagar","🏔️","Dal Lake, Gulmarg, Pahalgam"),
            ("South India Pilgrimage","PILGRIMAGE","Chennai to Rameswaram",5,6,9500,12500,"Train+hotel+temple entry","Chennai","Rameswaram","🛕","Meenakshi Temple, Rameswaram"),
            ("Goa Beach Special","BEACH","Mumbai to Goa",3,4,7800,10500,"Train+resort+breakfast","Mumbai","Goa","🌊","Baga Beach, Old Goa, Dudhsagar"),
            ("Darjeeling Hill Tour","HILL_STATION","Kolkata to Darjeeling",4,5,11200,15000,"Train+toy train+resort","Kolkata","Darjeeling","🌄","Toy Train, Tiger Hill, Tea Gardens"),
            ("Rajasthan Royal Tour","HERITAGE","Jaipur to Jodhpur to Udaipur",6,7,15000,19000,"Train+palace hotel+safaris","Jaipur","Udaipur","🏰","Amber Fort, Mehrangarh, Lake Pichola"),
        ]
        for name,cat,desc,nights,days,price,orig,incl,src,dst,emoji,hl in tours:
            TourPackage.objects.get_or_create(name=name, defaults={
                "category":cat,"description":desc,"itinerary":desc,
                "duration_nights":nights,"duration_days":days,
                "price_per_person":price,"original_price":orig,
                "inclusions":incl,"source_city":src,"destination_city":dst,
                "image_emoji":emoji,"highlights":hl,
            })
        self.stdout.write(self.style.SUCCESS("Services seed done!"))
