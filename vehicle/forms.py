from django import forms
from .models import DailyReport, Vehicle
from django.utils import timezone


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['report', 'date']
        labels = {
            'date': 'Дата отчета',
            'report': 'Отчет',
        }
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'report': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DailyReportForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(driver=user)
        self.fields['date'].initial = timezone.now().date().strftime('%Y-%m-%d')
