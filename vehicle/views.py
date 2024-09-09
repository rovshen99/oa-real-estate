from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DailyReportForm
from .models import Vehicle


@login_required
def submit_daily_report(request):
    try:
        user_vehicle = Vehicle.objects.get(driver=request.user)
    except Vehicle.DoesNotExist:
        return render(request, 'not_driver.html')

    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.vehicle = user_vehicle
            report.save()
            messages.success(request, 'Отчет успешно отправлен!')
            return render(request, 'report_submitted.html')
        else:
            messages.error(request, 'Ошибка отправки отчета. Пожалуйста, попробуйте еще раз.')
    else:
        form = DailyReportForm()

    print(user_vehicle.registration_number)
    return render(request, 'submit_daily_report.html', {'form': form, 'registration_number': user_vehicle.registration_number})


# def not_driver(request):
#     return render(request, 'not_driver.html')
#
#
# def report_submitted(request):
#     return render(request, 'report_submitted.html')
