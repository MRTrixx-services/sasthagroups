from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


def home(request):
    return render(request, "beauty/home.html")


def book_appointment(request):
    if request.method == 'POST':
        name           = request.POST.get('name', '').strip()
        phone          = request.POST.get('phone', '').strip()
        email          = request.POST.get('email', '').strip()
        service        = request.POST.get('service', '').strip()
        preferred_date = request.POST.get('preferred_date', '').strip()
        notes          = request.POST.get('notes', '').strip()

        if not name or not phone or not service:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('beauty:home')

        ctx = {
            'name':           name,
            'phone':          phone,
            'email':          email,
            'service':        service,
            'preferred_date': preferred_date,
            'notes':          notes,
            'submitted_at':   timezone.now().strftime('%d %b %Y, %I:%M %p'),
        }

        admin_html = render_to_string('beauty/email/booking_admin.html', ctx)
        admin_msg = EmailMultiAlternatives(
            subject=f'[Sastha Beauty] New Booking – {service} from {name}',
            body=f'New booking: {name} ({phone}) for {service}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['info@sasthagroup.com'],
            reply_to=[email] if email else [],
        )
        admin_msg.attach_alternative(admin_html, 'text/html')

        if email:
            user_html = render_to_string('beauty/email/booking_user.html', ctx)
            user_msg = EmailMultiAlternatives(
                subject='Your Appointment Request – Sastha Beauty Parlour 🌸',
                body=f'Hi {name}, we received your booking request for {service}. We will WhatsApp you at {phone} to confirm.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            user_msg.attach_alternative(user_html, 'text/html')

        try:
            admin_msg.send()
            if email:
                user_msg.send()
        except Exception:
            pass

        messages.success(request, f'Thank you {name}! Your booking request for {service} has been received. We will WhatsApp you shortly to confirm. 🌸')
        return redirect('beauty:home')

    return redirect('beauty:home')
