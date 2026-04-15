from django.core.management.base import BaseCommand
from trains.models import Station, Train, CoachClass, SeatAvailability
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds database with sample Indian Railways data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding stations...')
        stations_data = [
            ('CSTM','Mumbai CST','Mumbai','Maharashtra','CR'),
            ('NDLS','New Delhi','New Delhi','Delhi','NR'),
            ('HWH','Howrah Junction','Kolkata','West Bengal','ER'),
            ('MAS','Chennai Central','Chennai','Tamil Nadu','SR'),
            ('SBC','KSR Bengaluru City','Bengaluru','Karnataka','SWR'),
            ('SC','Secunderabad Junction','Hyderabad','Telangana','SCR'),
            ('ADI','Ahmedabad Junction','Ahmedabad','Gujarat','WR'),
            ('PUNE','Pune Junction','Pune','Maharashtra','CR'),
            ('JP','Jaipur Junction','Jaipur','Rajasthan','NWR'),
            ('LKO','Lucknow Charbagh','Lucknow','Uttar Pradesh','NR'),
            ('PNBE','Patna Junction','Patna','Bihar','ECR'),
            ('BPL','Bhopal Junction','Bhopal','Madhya Pradesh','WCR'),
            ('NGP','Nagpur Junction','Nagpur','Maharashtra','CR'),
            ('ST','Surat','Surat','Gujarat','WR'),
            ('BSB','Varanasi Junction','Varanasi','Uttar Pradesh','NER'),
            ('AGC','Agra Cantt','Agra','Uttar Pradesh','NCR'),
        ]
        stations = {}
        for code, name, city, state, zone in stations_data:
            s, _ = Station.objects.get_or_create(code=code, defaults={
                'name': name, 'city': city, 'state': state, 'zone': zone
            })
            stations[code] = s
        self.stdout.write(f'  {len(stations)} stations ready')

        self.stdout.write('Seeding trains...')
        trains_data = [
            ('12301','Howrah Rajdhani Express','RAJ','CSTM','NDLS','16:35','10:05',17*60+30,1390,True,True,True,True,True,True,True,True),
            ('12951','Mumbai Rajdhani Express','RAJ','CSTM','NDLS','17:40','08:35',14*60+55,1384,True,False,True,False,True,False,True,True),
            ('22209','Mumbai Duronto Express','DUR','CSTM','NDLS','23:10','15:55',16*60+45,1384,False,True,False,True,False,True,False,False),
            ('12137','Punjab Mail','MAIL','CSTM','NDLS','19:05','14:30',19*60+25,1542,True,True,True,True,True,True,True,False),
            ('12261','Howrah Duronto Express','DUR','CSTM','HWH','08:15','06:00',21*60+45,1968,True,False,True,False,True,False,True,False),
            ('12009','Mumbai Shatabdi Express','SHT','CSTM','PUNE','06:25','08:30',2*60+5,192,True,True,True,True,True,True,False,False),
            ('12431','Rajdhani Express','RAJ','NDLS','HWH','16:55','09:55',17*60+0,1450,True,True,True,True,True,True,True,True),
            ('12621','Tamil Nadu Express','SF','NDLS','MAS','22:30','07:10',32*60+40,2175,True,True,True,True,True,True,True,False),
            ('12649','Karnataka Sampark Kranti','SF','NDLS','SBC','20:00','08:30',36*60+30,2444,True,False,True,False,True,False,True,False),
            ('12001','Bhopal Shatabdi','SHT','NDLS','BPL','06:00','13:55',7*60+55,705,True,True,True,True,True,True,False,False),
        ]
        coach_configs = {
            'RAJ':  [('1A',18,4800,5500),('2A',46,2900,3400),('3A',64,2050,2450)],
            'SHT':  [('CC',78,1200,1500),('2A',46,2400,2900)],
            'DUR':  [('1A',18,4200,5000),('2A',46,2500,3000),('3A',64,1800,2200),('SL',72,620,900)],
            'MAIL': [('2A',46,2200,2700),('3A',64,1600,2000),('SL',72,520,780),('GN',90,200,0)],
            'SF':   [('2A',46,2400,2900),('3A',64,1750,2100),('SL',72,580,850),('GN',90,200,0)],
        }
        train_objs = []
        for row in trains_data:
            t, _ = Train.objects.get_or_create(number=row[0], defaults={
                'name':row[1],'train_type':row[2],
                'source_station':stations[row[3]],'destination_station':stations[row[4]],
                'departure_time':row[5],'arrival_time':row[6],
                'duration_minutes':row[7],'distance_km':row[8],
                'runs_on_mon':row[9],'runs_on_tue':row[10],'runs_on_wed':row[11],
                'runs_on_thu':row[12],'runs_on_fri':row[13],'runs_on_sat':row[14],
                'runs_on_sun':row[15],'pantry_car':row[16],'is_active':True
            })
            for cls, seats, fare, tatkal in coach_configs.get(row[2], coach_configs['SF']):
                CoachClass.objects.get_or_create(train=t, coach_class=cls, defaults={
                    'total_seats':seats,'base_fare':fare,'tatkal_fare':tatkal,'coach_count':2
                })
            train_objs.append(t)
        self.stdout.write(f'  {len(train_objs)} trains ready')

        self.stdout.write('Seeding seat availability for next 60 days...')
        today = date.today()
        count = 0
        for t in train_objs:
            for cc in t.coach_classes.all():
                for d in range(1, 61):
                    jdate = today + timedelta(days=d)
                    seats = random.randint(0, cc.total_seats)
                    wl = random.randint(0, 20) if seats == 0 else 0
                    _, created = SeatAvailability.objects.get_or_create(
                        coach_class=cc, journey_date=jdate,
                        defaults={'available_seats': seats, 'waitlist_count': wl}
                    )
                    if created:
                        count += 1
        self.stdout.write(f'  {count} availability records created')
        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully!'))
