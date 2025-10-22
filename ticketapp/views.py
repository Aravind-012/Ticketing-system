from django.shortcuts import render, redirect
from .models import Ticket
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

# dashboard
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.timezone import now, timedelta
from .models import Ticket  # adjust import if needed

# newclient
from .models import ClientOnboarding

# payment pending   
from datetime import datetime

def parse_ym_to_date(ym_str):
    if ym_str:
        return datetime.strptime(ym_str + "-01", "%Y-%m-%d").date()
    return None

# def ticket_list(request):
#     tickets = Ticket.objects.all().order_by("-created_at")
#     return render(request, "ticket_details.html", {"tickets": tickets})
# def ticket_list(request):
#     tickets = Ticket.objects.select_related('assigned_to').all().order_by("-created_at")
#     return render(request, "ticket_list.html", {"tickets": tickets})


def ticket_create(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        requester_name = request.POST.get("requester_name")
        requester_email = request.POST.get("requester_email")
        requester_phone = request.POST.get("requester_phone")
        priority = request.POST.get("priority")
        assigned_to = request.POST.get("assigned_to")
        assigned_phone = request.POST.get("assigned_phone", "").strip()
        # Save into MySQL
        Ticket.objects.create(
            subject=subject,
            requester_name=requester_name,
            requester_email=requester_email,
            requester_phone=requester_phone,
            priority=priority,
            assigned_to=assigned_to,
            assigned_phone=assigned_phone,
        )
        return redirect("ticket_list")  # ✅ Redirect back to list

    return render(request, "ticket_create.html")


def update_ticket_status(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        new_status = request.POST.get("status")
        if new_status in ["Pending", "Work in Process", "Completed"]:
            ticket.status = new_status
            # Clear escalation only when status is completed
            if new_status == "Completed":
                ticket.is_escalated = False  
            ticket.save()
    return redirect("ticket_list")

def ticket_filter(request):
    status = request.GET.get('status')  # Get status from URL query parameter

    if status in ['Pending', 'Work in Process', 'Completed']:
        tickets = Ticket.objects.filter(status=status).order_by("-created_at")
    else:
        tickets = Ticket.objects.all().order_by("-created_at")  # Default: all tickets

    return render(request, 'ticket_filter.html', {'tickets': tickets, 'selected_status': status})

# def ticket_volume_dashboard(request):
#     start_date = now() - timedelta(days=30)

#     created_per_day = (
#         Ticket.objects.filter(created_at__gte=start_date)
#         .annotate(day=TruncDay('created_at'))
#         .values('day')
#         .annotate(count=Count('id'))
#         .order_by('day')
#     )

#     resolved_per_day = (
#         Ticket.objects.filter(status='Completed', updated_at__gte=start_date)
#         .annotate(day=TruncDay('created_at'))
#         .values('day')
#         .annotate(count=Count('id'))
#         .order_by('day')
#     )

#     dates = [entry['day'].date() for entry in created_per_day]
#     created_dict = {entry['day'].date(): entry['count'] for entry in created_per_day}
#     resolved_dict = {entry['day'].date(): entry['count'] for entry in resolved_per_day}

#     pending_counts = []
#     running_total = 0
#     for date in dates:
#         daily_created = created_dict.get(date, 0)
#         daily_resolved = resolved_dict.get(date, 0)
#         running_total += daily_created - daily_resolved
#         pending_counts.append(running_total if running_total > 0 else 0)

#     context = {
#         'dates': [date.strftime('%Y-%m-%d') for date in dates],
#         'created_counts': [created_dict.get(date, 0) for date in dates],
#         'resolved_counts': [resolved_dict.get(date, 0) for date in dates],
#         'pending_counts': pending_counts,
#     }
#     return render(request, 'ticket_volume_dashboard.html', context)

def client_status(request):
    return render(request, 'client_status.html')
def client_onboarding_add(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name")
        client_phone = request.POST.get("client_phone")
        description = request.POST.get("description", "")
        plan = request.POST.get("plans")
        assigned_to = request.POST.get("assigned_to")
        assigned_phone=request.POST.get("assigned_phone", ""),
        onboarding_deadline_days=int(request.POST.get("onboarding_deadline_days", 7))

        ClientOnboarding.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            description=description,
            plan=plan,
            assigned_to=assigned_to,
            assigned_phone=assigned_phone,
            onboarding_deadline_days=onboarding_deadline_days,
        )
        return redirect('client_onboarding_list')
    return render(request, 'client_onboarding_add.html')  # Or show a "success" message

    
def client_onboarding_list(request):
    clients = ClientOnboarding.objects.order_by('-created_at')
    return render(request, 'client_onboarding_list.html', {'clients': clients})

from django.shortcuts import get_object_or_404, redirect

def update_client_status(request, pk):
    if request.method == 'POST':
        client = get_object_or_404(ClientOnboarding, pk=pk)
        new_status = request.POST.get('status')
        print(f"Updating client {client.id} status to {new_status}")  # debugging
        if new_status in dict(ClientOnboarding.STATUS_CHOICES):
            client.status = new_status
            client.save()
    return redirect('client_onboarding_list')


from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.timezone import now, timedelta
from .models import ClientOnboarding

def onboarding_dashboard(request):
    # Define time range (last 30 days)
    start_date = now() - timedelta(days=30)

    # Aggregate numbers of completed onboarding per day
    onboarded = (
        ClientOnboarding.objects.filter(status='completed', created_at__gte=start_date)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Aggregate numbers of pending onboarding per day
    pending = (
        ClientOnboarding.objects.filter(status='pending', created_at__gte=start_date)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    # Prepare date labels and data arrays for chart.js
    dates = [entry['day'].date() for entry in onboarded]
    onboarded_dict = {entry['day'].date(): entry['count'] for entry in onboarded}
    pending_dict = {entry['day'].date(): entry['count'] for entry in pending}
    onboarding_dates = [date.strftime('%Y-%m-%d') for date in dates]
    onboarded_counts = [onboarded_dict.get(date, 0) for date in dates]
    pending_counts = [pending_dict.get(date, 0) for date in dates]

    # Overall stats
    total_clients = ClientOnboarding.objects.count()
    pending_clients = ClientOnboarding.objects.filter(status='pending').count()
    completed_clients = ClientOnboarding.objects.filter(status='completed').count()

    context = {
        'total_clients': total_clients,
        'pending_clients': pending_clients,
        'completed_clients': completed_clients,
        'onboarding_dates': onboarding_dates,
        'onboarded_counts': onboarded_counts,
        'pending_counts': pending_counts,
    }
    print("Total clients:", total_clients)
    print("Pending clients:", pending_clients)
    print("Completed clients:", completed_clients)
    print("Dates:", onboarding_dates)
    print("Completed counts:", onboarded_counts)
    print("Pending counts:", pending_counts)

    return render(request, 'ticket_volume_dashboard.html', context)

def ticket_volume_dashboard(request):
    start_date = now() - timedelta(days=30)

    # Ticket data aggregation as before
    created_per_day = (
        Ticket.objects.filter(created_at__gte=start_date)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    resolved_per_day = (
        Ticket.objects.filter(status='Completed', updated_at__gte=start_date)
        .annotate(day=TruncDay('updated_at'))  # fixed to use updated_at
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    dates = [entry['day'].date() for entry in created_per_day]
    created_dict = {entry['day'].date(): entry['count'] for entry in created_per_day}
    resolved_dict = {entry['day'].date(): entry['count'] for entry in resolved_per_day}

    pending_counts = []
    running_total = 0
    for date in dates:
        daily_created = created_dict.get(date, 0)
        daily_resolved = resolved_dict.get(date, 0)
        running_total += daily_created - daily_resolved
        pending_counts.append(running_total if running_total > 0 else 0)

    # Client onboarding data
    client_start_date = now() - timedelta(days=30)
    onboarded = (
        ClientOnboarding.objects.filter(status='completed', created_at__gte=client_start_date)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    pending_onboarded = (
        ClientOnboarding.objects.filter(status='pending', created_at__gte=client_start_date)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    onboarding_dates = [entry['day'].date() for entry in onboarded]
    onboarded_counts = {entry['day'].date(): entry['count'] for entry in onboarded}
    pending_counts_onboarded = {entry['day'].date(): entry['count'] for entry in pending_onboarded}

    onboarding_dates_str = [date.strftime('%Y-%m-%d') for date in onboarding_dates]
    onboarded_values = [onboarded_counts.get(date, 0) for date in onboarding_dates]
    pending_values = [pending_counts_onboarded.get(date, 0) for date in onboarding_dates]

    stat_total_clients = ClientOnboarding.objects.count()
    stat_pending_clients = ClientOnboarding.objects.filter(status='pending').count()
    stat_completed_clients = ClientOnboarding.objects.filter(status='completed').count()

    context = {
        # Ticket context
        'dates': [date.strftime('%Y-%m-%d') for date in dates],
        'created_counts': [created_dict.get(date, 0) for date in dates],
        'resolved_counts': [resolved_dict.get(date, 0) for date in dates],
        'pending_counts': pending_counts,

        # Client onboarding context
        'total_clients': stat_total_clients,
        'pending_clients': stat_pending_clients,
        'completed_clients': stat_completed_clients,
        'onboarding_dates': onboarding_dates_str,
        'onboarded_counts': onboarded_values,
        'pending_counts_onboarded': pending_values,
    }

    return render(request, 'ticket_volume_dashboard.html', context)

from django.shortcuts import render, redirect
from .models import PaymentPendingClient
from django.contrib.auth.models import User


def add_payment_pending_client(request):
    users = User.objects.all()  # to populate dropdown

    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_phone = request.POST.get('client_phone')
        assigned_to = request.POST.get('assigned_to')  # This is username string
        assigned_phone = request.POST.get('assigned_phone')
        payment_amount = request.POST.get('payment_amount')
        due_date = request.POST.get('due_date')
        
        # New fields related to subscription duration
        duration = request.POST.get('duration')
        months = request.POST.get('months') or None
        # start_month = request.POST.get('start_month') or None
        # end_month = request.POST.get('end_month') or None
        years = request.POST.get('years') or None
        start_year = request.POST.get('start_year') or None
        end_year = request.POST.get('end_year') or None
        # Convert year-month strings to full dates for DateFields
        start_month_str = request.POST.get('start_month')
        end_month_str = request.POST.get('end_month')
        start_month = parse_ym_to_date(start_month_str)
        end_month = parse_ym_to_date(end_month_str)

        # Create and save new PaymentPendingClient using username string
        PaymentPendingClient.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            assigned_to=assigned_to,
            assigned_phone=assigned_phone,
            payment_amount=payment_amount,
            due_date=due_date,
            duration=duration,
            months=months,
            start_month=start_month,
            end_month=end_month,
            years=years,
            start_year=start_year,
            end_year=end_year,
        )
        return redirect('payment_pending_list')  # Redirect after creating

    return render(request, 'add_payment_pending_client.html', {'users': users})


# from .models import PaymentPendingClient

# def payment_pending_list(request):
#     clients = PaymentPendingClient.objects.all()
#     return render(request, 'payment_pending_list.html', {'clients': clients})
from datetime import date
from .models import PaymentPendingClient

def payment_pending_list(request):
    clients = PaymentPendingClient.objects.all()
    today = date.today()
    for client in clients:
        client.is_overdue = client.due_date and today > client.due_date
    return render(request, 'payment_pending_list.html', {'clients': clients})

from django.views.decorators.http import require_POST

@require_POST
def update_payment_status(request, client_id):
    status = request.POST.get('status')
    client = PaymentPendingClient.objects.get(pk=client_id)
    if status in ['pending', 'completed']:
        client.status = status
        client.save()
    return redirect('payment_pending_list')

from django.shortcuts import get_object_or_404

def delete_payment_pending_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(PaymentPendingClient, id=client_id)
        client.delete()
    return redirect('payment_pending_list')

from django.shortcuts import get_object_or_404, redirect

def client_onboarding_delete(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(ClientOnboarding, id=client_id)
        client.delete()
    return redirect('client_onboarding_list')

from django.shortcuts import get_object_or_404, redirect
from .models import Ticket

def ticket_delete(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
    return redirect('ticket_list')

from django.core.paginator import Paginator

def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")
    paginator = Paginator(tickets, 10)  # 10 tickets per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "ticket_details.html", {"page_obj": page_obj})


