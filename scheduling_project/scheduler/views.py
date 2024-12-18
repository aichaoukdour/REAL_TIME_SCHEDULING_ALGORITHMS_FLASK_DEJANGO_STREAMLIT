from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import ProcessForm
from django.contrib.sessions.models import Session
from .algorithms.FCFS.FCFS import fcfs
from .algorithms.SJF.SJF_without_preemption import sjf_without_preemption
from .algorithms.preemptif_SJF.SJF_with_preemption import sjf_with_preemption
from .algorithms.gantt_chart_drawer import gantt_chart
from .algorithms.RM.rm_runner import rm_runner
from .algorithms.DM.dm_runner import dm_runner
from .algorithms.EDF.edf_runner import edf_function
from .algorithms.LLF.llf_runner import llf_function

# Initialize session data
def initialize_session(request):
    if 'SESSION_DATA' not in request.session:
        request.session['SESSION_DATA'] = {
            "Task": [], "Burst Time": [], "Arrival Time": [], "Deadline": [], "Period": []
        }

def index(request):
    return render(request, 'index.html')

# FCFS and SJF (Non-Preemptive & Preemptive) Scheduling Page
def fcfs_sjf_page(request):
    initialize_session(request)
    session_data = request.session['SESSION_DATA']

    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            new_burst_time = form.cleaned_data['burst_time']
            new_arrival_time = form.cleaned_data['arrival_time']

            session_data['Task'].append(f"T{len(session_data['Task']) + 1}")
            session_data['Burst Time'].append(new_burst_time)
            session_data['Arrival Time'].append(new_arrival_time)
            request.session['SESSION_DATA'] = session_data
            return redirect('fcfs_sjf_page')
    else:
        form = ProcessForm()

    # Algorithm selection logic
    algorithm = request.GET.get('algorithm')
    response = {}
    gantt_chart_html = None

    if algorithm:
        processes = [{"Process ID": i + 1, "Task": session_data["Task"][i],
                      "Arrival Time": session_data["Arrival Time"][i],
                      "Burst Time": session_data["Burst Time"][i]}
                     for i in range(len(session_data["Burst Time"]))]

        if algorithm == "FCFS":
            waiting_times, avg_waiting_time, chart = fcfs(processes)
        elif algorithm == "SJF Without Preemption":
            waiting_times, avg_waiting_time, chart = sjf_without_preemption(processes)
        elif algorithm == "SJF With Preemption":
            waiting_times, avg_waiting_time, chart = sjf_with_preemption(processes)

        response = {"waiting_times": waiting_times, "avg_waiting_time": avg_waiting_time}
        gantt_chart_html = gantt_chart(chart)

    tasks = zip(session_data['Task'], session_data['Arrival Time'], session_data['Burst Time'])
    return render(request, 'fcfs_sjf.html', {'form': form, 'tasks': tasks, 'response': response, 'gantt_chart_html': gantt_chart_html})

# Process update page
def update_process(request):
    initialize_session(request)
    if request.method == 'POST':
        task_id = request.POST['task_id']
        new_burst_time = int(request.POST['burst_time'])
        new_arrival_time = int(request.POST['arrival_time'])
        task_index = request.session['SESSION_DATA']['Task'].index(task_id)
        request.session['SESSION_DATA']['Burst Time'][task_index] = new_burst_time
        request.session['SESSION_DATA']['Arrival Time'][task_index] = new_arrival_time
        request.session.modified = True
    return redirect('fcfs_sjf_page')

# Process delete page
def delete_process(request):
    initialize_session(request)
    task_id = request.GET.get('task')
    
    if not task_id:
        return HttpResponse("Task ID not provided.", status=400)
    
    session_data = request.session['SESSION_DATA']

    if 'Task' in session_data and session_data['Task']:
        try:
            task_index = session_data['Task'].index(task_id)
            for key in session_data:
                if session_data[key]:
                    session_data[key].pop(task_index)
            request.session.modified = True
            return redirect('fcfs_sjf_page')
        except ValueError:
            return HttpResponse(f"Task '{task_id}' not found.", status=404)
    else:
        return HttpResponse("No tasks to delete.", status=400)

# DM, RM, EDF, LLF Scheduling Page
def dm_rm_edf_llf_page(request):
    initialize_session(request)
    session_data = request.session['SESSION_DATA']

    # Check for missing keys or inconsistencies in session data
    required_keys = ["Task", "Arrival Time", "Burst Time", "Deadline", "Period"]
    for key in required_keys:
        if key not in session_data:
            session_data[key] = []  # Initialize missing keys with empty lists

    # Ensure that all lists are the same length
    min_length = min(len(session_data[key]) for key in required_keys)
    for key in required_keys:
        session_data[key] = session_data[key][:min_length]  # Trim lists to the same length

    # Save changes back to the session
    request.session['SESSION_DATA'] = session_data
    request.session.modified = True

    if request.method == 'POST':
        try:
            new_burst_time = int(request.POST['burst_time'])
            new_arrival_time = int(request.POST['arrival_time'])
            new_deadline = int(request.POST['deadline'])
            new_period = int(request.POST['period'])

            # Add new task with all required attributes
            session_data['Task'].append(f"T{len(session_data['Task']) + 1}")
            session_data['Arrival Time'].append(new_arrival_time)
            session_data['Burst Time'].append(new_burst_time)
            session_data['Deadline'].append(new_deadline)
            session_data['Period'].append(new_period)

            # Save updated session data
            request.session['SESSION_DATA'] = session_data
            request.session.modified = True
        except ValueError:
            return HttpResponse("Invalid input, please enter integers for all fields.", status=400)

        return redirect('dm_rm_edf_llf_page')

    data = session_data
    zipped_data = zip(data['Task'], data['Arrival Time'], data['Burst Time'], data['Deadline'], data['Period'])
    zipped_data_list = list(zipped_data)

    algorithm = request.GET.get('algorithm')
    response = {}
    gantt_chart_html = None

    if algorithm:
        # Create a list of processes based on consistent session data
        processes = [{"Process ID": i + 1, "Task": data["Task"][i],
                      "Arrival Time": data["Arrival Time"][i],
                      "Burst Time": data["Burst Time"][i],
                      "Deadline": data["Deadline"][i],
                      "Period": data["Period"][i]}
                     for i in range(len(data["Task"]))]

        # Run the selected algorithm
        if algorithm == "RM":
            cpu_occupation, chart = rm_runner(processes)
        elif algorithm == "DM":
            cpu_occupation, chart = dm_runner(processes)
        elif algorithm == "EDF":
            cpu_occupation, chart = edf_function(processes)
        elif algorithm == "LLF":
            cpu_occupation, chart = llf_function(processes)

        # Prepare response and Gantt chart
        response = {"cpu_occupation": cpu_occupation}
        gantt_chart_html = gantt_chart(chart)

    return render(request, 'dm_rm_edf_llf.html', {'data': zipped_data_list, 'response': response, 'gantt_chart_html': gantt_chart_html})

# Update process for DM, RM, EDF, LLF algorithms
def update_process_dm_rm_edf_llf(request):
    initialize_session(request)
    if request.method == 'POST':
        task_id = request.POST['task_id']
        try:
            new_burst_time = int(request.POST['burst_time'])
            new_arrival_time = int(request.POST['arrival_time'])

            task_index = request.session['SESSION_DATA']['Task'].index(task_id)
            request.session['SESSION_DATA']['Burst Time'][task_index] = new_burst_time
            request.session['SESSION_DATA']['Arrival Time'][task_index] = new_arrival_time
            request.session.modified = True
        except ValueError:
            return HttpResponse("Invalid input, please enter integers for Burst Time and Arrival Time.", status=400)

    return redirect('dm_rm_edf_llf_page')
