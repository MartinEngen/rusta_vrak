from django.shortcuts import render


from django.contrib.auth.decorators import user_passes_test

from forms import LockReservationsForm
from models import lock_reservation_period
import datetime

@user_passes_test(lambda u: u.is_staff)
def index_control_panel(request):
    return render(request, 'control_panel/index_control_panel.html')



@user_passes_test(lambda u: u.is_staff)
def reservation_locks(request):

    # Standard Return function
    def lock_reservation_page():
        # Get all reservation locks.
        # Except the ones with dates in the past.

        existing_reservation_locks = lock_reservation_period.objects.filter(to_date__gte=datetime.date.today())

        return render(
            request,
            'control_panel/lock_reservation_period.html',
            {'existing_reservation_locks': existing_reservation_locks}
        )

    # POST REQUEST
    if request.method == 'POST':
        form = LockReservationsForm(request.POST)

        # If the form contains two valid dates.
        if form.is_valid():
            posted_from_date = form.cleaned_data['from_date']
            posted_to_date = form.cleaned_data['to_date']

            print posted_to_date

            # If the dates are in the wrong order, reorder.
            if posted_from_date > posted_to_date:
                placeholder = posted_from_date
                from_date = posted_to_date
                posted_to_date = placeholder



            new_lock = lock_reservation_period(
                creator=request.user,
                from_date=posted_from_date,
                to_date=posted_to_date
            )

            new_lock.save()

            return lock_reservation_page()

        else:
            return lock_reservation_page()

    # GET REQUEST
    else:
        return lock_reservation_page()
