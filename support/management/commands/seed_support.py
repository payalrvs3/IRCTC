from django.core.management.base import BaseCommand
from support.models import FAQ

class Command(BaseCommand):
    help = "Seeds FAQ data"
    def handle(self, *args, **kwargs):
        faqs = [
            ("How do I cancel my ticket?","Log in, go to My Bookings, select booking, click Cancel. Refunds in 5-7 days.","BOOKING",1),
            ("What is Tatkal booking?","Opens 1 day before at 10 AM for AC, 11 AM for non-AC classes.","BOOKING",2),
            ("What payment options are available?","UPI, Net Banking, Debit/Credit Cards, IRCTC Wallet.","PAYMENT",1),
            ("My payment failed but amount was deducted?","Refund auto-processed in 5-7 days. Raise a ticket if longer.","PAYMENT",2),
            ("Why is my PNR on Waitlist?","Confirmed when others cancel. Auto-cancelled before departure if not confirmed.","PNR",1),
            ("What does RAC mean?","Reservation Against Cancellation — shared berth that may become full berth.","PNR",2),
            ("How do I download my e-ticket?","Available in My Bookings or via confirmation email.","ACCOUNT",1),
            ("How does e-Catering work?","Enter PNR, select station and items, pay online — food delivered to seat.","CATERING",1),
            ("What if train is cancelled by Railways?","Full automatic refund within 5 working days, no charges.","GENERAL",1),
        ]
        count = sum(1 for q,a,s,o in faqs if FAQ.objects.get_or_create(question=q,defaults={"answer":a,"section":s,"order":o})[1])
        self.stdout.write(self.style.SUCCESS(f"Seeded {count} FAQs!"))
