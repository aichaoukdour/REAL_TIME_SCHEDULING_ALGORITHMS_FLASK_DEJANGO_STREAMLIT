from django import forms

class ProcessForm(forms.Form):
    burst_time = forms.IntegerField(label="Burst Time")
    arrival_time = forms.IntegerField(label="Arrival Time")
    deadline = forms.IntegerField(label="Deadline", required=False)
    period = forms.IntegerField(label="Period", required=False)
