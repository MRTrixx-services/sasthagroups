from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


FLOWER_LABELS = {
    'marigold': 'Marigold Garlands',
    'mogra':    'Mogra Gajra',
    'rose':     'Rose Bouquets',
    'pooja':    'Pooja Flowers',
    'rangoli':  'Rangoli Petal Set',
    'wedding':  'Wedding & Event Decor',
    'other':    'Other / General Enquiry',
}


def home(request):
    return render(request, "flowers/flowers.html")


def flower_enquiry(request):
    if request.method == 'POST':
        name          = request.POST.get('name', '').strip()
        phone         = request.POST.get('phone', '').strip()
        email         = request.POST.get('email', '').strip()
        service       = request.POST.get('service', '').strip()
        delivery_date = request.POST.get('date', '').strip()
        message       = request.POST.get('message', '').strip()

        if not name or not phone or not service:
            messages.error(request, 'Please fill in your name, phone and select a flower type.')
            return redirect('flowers:home')

        ctx = {
            'name':           name,
            'phone':          phone,
            'email':          email,
            'flower_display': FLOWER_LABELS.get(service, service),
            'delivery_date':  delivery_date,
            'message':        message,
            'submitted_at':   timezone.now().strftime('%d %b %Y, %I:%M %p'),
        }

        # Admin email
        admin_html = render_to_string('flowers/email/enquiry_admin.html', ctx)
        admin_msg = EmailMultiAlternatives(
            subject=f"[Sastha Flowers] New Enquiry – {ctx['flower_display']} from {name}",
            body=f"New flower enquiry from {name} ({phone}) for {ctx['flower_display']}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['info@sasthagroup.com'],
            reply_to=[email] if email else [],
        )
        admin_msg.attach_alternative(admin_html, 'text/html')

        # User confirmation email
        if email:
            user_html = render_to_string('flowers/email/enquiry_user.html', ctx)
            user_msg = EmailMultiAlternatives(
                subject=f"Your Flower Enquiry Received – Sastha Flower Shop 🌸",
                body=f"Hi {name}, we received your enquiry for {ctx['flower_display']}. We will WhatsApp you at {phone} shortly.",
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

        messages.success(
            request,
            f"Thank you {name}! Your enquiry for {ctx['flower_display']} has been received. We'll WhatsApp you shortly. 🌸"
        )
        return redirect('flowers:home')

    return redirect('flowers:home')
