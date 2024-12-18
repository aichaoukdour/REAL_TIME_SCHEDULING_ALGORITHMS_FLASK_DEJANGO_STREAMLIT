from flask import Flask, render_template, request, redirect, url_for, session
from FCFS.FCFS import fcfs
from LLF.llf_runner import llf_function
from EDF.edf_runner import edf_function
from SJF.SJF_without_preemption import sjf_without_preemption
from preemptif_SJF.SJF_with_preemption import sjf_with_preemption
from RM.rm_runner import rm_runner
from DM.dm_runner import dm_runner
from gantt_chart_drawer import gantt_chart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize session data
@app.before_request
def initialize_session_data():
    if 'SESSION_DATA' not in session:
        session['SESSION_DATA'] = {"Task": [], "Burst Time": [], "Arrival Time": [], "Deadline": [], "Period": []}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/fcfs_sjf', methods=['GET', 'POST'])
def fcfs_sjf_page():
    if request.method == 'POST':
        try:
            new_burst_time = int(request.form['burst_time'])
            new_arrival_time = int(request.form['arrival_time'])

            # Add new task safely
            session['SESSION_DATA']["Task"].append(f"T{len(session['SESSION_DATA']['Arrival Time']) + 1}")
            session['SESSION_DATA']["Burst Time"].append(new_burst_time)
            session['SESSION_DATA']["Arrival Time"].append(new_arrival_time)
            session.modified = True  # Notify Flask that session has changed
        except ValueError:
            return "Invalid input, please enter integers for Burst Time and Arrival Time."

        return redirect(url_for('fcfs_sjf_page'))

    if 'algorithm' in request.args:
        algorithm = request.args.get('algorithm')
        data = session['SESSION_DATA']

        # Prepare processes for algorithms
        processes = [{"Process ID": i + 1, "Task": data["Task"][i],
                      "Arrival Time": data["Arrival Time"][i],
                      "Burst Time": data["Burst Time"][i]}
                     for i in range(len(data["Burst Time"]))]

        # Execute the selected algorithm
        if algorithm == "FCFS":
            waiting_times, avg_waiting_time, chart = fcfs(processes)
        elif algorithm == "SJF Without Preemption":
            waiting_times, avg_waiting_time, chart = sjf_without_preemption(processes)
        else:
            waiting_times, avg_waiting_time, chart = sjf_with_preemption(processes)

        # Render response and Gantt chart
        response = {"waiting_times": waiting_times, "avg_waiting_time": avg_waiting_time}
        gantt_chart_html = gantt_chart(chart)
        return render_template("fcfs_sjf.html", response=response, gantt_chart_html=gantt_chart_html)

    # Pass task data to the template
    data = session['SESSION_DATA']
    tasks = zip(data['Task'], data['Arrival Time'], data['Burst Time'])
    return render_template("fcfs_sjf.html", tasks=tasks)

@app.route('/dm_rm_edf_llf', methods=['GET', 'POST'])
def dm_rm_edf_llf_page():
    if request.method == 'POST':
        try:
            new_burst_time = int(request.form['burst_time'])
            new_arrival_time = int(request.form['arrival_time'])
            new_deadline = int(request.form['deadline'])
            new_period = int(request.form['period'])

            # Add new task safely
            session['SESSION_DATA']["Task"].append(f"T{len(session['SESSION_DATA']['Arrival Time']) + 1}")
            session['SESSION_DATA']["Arrival Time"].append(new_arrival_time)
            session['SESSION_DATA']["Burst Time"].append(new_burst_time)
            session['SESSION_DATA']["Deadline"].append(new_deadline)
            session['SESSION_DATA']["Period"].append(new_period)
            session.modified = True
        except ValueError:
            return "Invalid input, please enter integers for all fields."

        return redirect(url_for('dm_rm_edf_llf_page'))

    # Combine data for template
    data = session['SESSION_DATA']
    zipped_data = zip(data['Task'], data['Arrival Time'], data['Burst Time'], data['Deadline'], data['Period'])
    zipped_data_list = list(zipped_data)

    if 'algorithm' in request.args:
        algorithm = request.args.get('algorithm')
        processes = [{"Process ID": i + 1, "Task": data["Task"][i],
                      "Arrival Time": data["Arrival Time"][i],
                      "Burst Time": data["Burst Time"][i],
                      "Deadline": data["Deadline"][i],
                      "Period": data["Period"][i]}
                     for i in range(len(data["Burst Time"]))]

        # Execute the selected algorithm
        if algorithm == "RM":
            cpu_occupation, chart = rm_runner(processes)
        elif algorithm == "DM":
            cpu_occupation, chart = dm_runner(processes)
        elif algorithm == "EDF":
            cpu_occupation, chart = edf_function(processes)
        elif algorithm == "LLF":
            cpu_occupation, chart = llf_function(processes)

        response = {"cpu_occupation": cpu_occupation}
        gantt_chart_html = gantt_chart(chart)
        return render_template("dm_rm_edf_llf.html", response=response, gantt_chart_html=gantt_chart_html)

    return render_template("dm_rm_edf_llf.html", data=zipped_data_list)

@app.route('/update_process', methods=['POST'])
def update_process():
    task_id = request.form['task_id']
    try:
        new_burst_time = int(request.form['burst_time'])
        new_arrival_time = int(request.form['arrival_time'])

        # Find the index of the task and update
        task_index = session['SESSION_DATA']['Task'].index(task_id)
        session['SESSION_DATA']['Burst Time'][task_index] = new_burst_time
        session['SESSION_DATA']['Arrival Time'][task_index] = new_arrival_time
        session.modified = True
    except ValueError:
        return "Invalid input, please enter integers for Burst Time and Arrival Time."

    return redirect(url_for('fcfs_sjf_page'))

@app.route('/delete_process', methods=['GET'])
def delete_process():
    task_id = request.args.get('task')
    if task_id in session['SESSION_DATA']['Task']:
        task_index = session['SESSION_DATA']['Task'].index(task_id)
        for key in session['SESSION_DATA']:
            session['SESSION_DATA'][key].pop(task_index)
        session.modified = True
    return redirect(url_for('fcfs_sjf_page'))

if __name__ == '__main__':
    app.run(debug=True)
