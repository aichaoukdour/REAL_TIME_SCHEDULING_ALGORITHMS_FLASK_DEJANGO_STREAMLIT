def fcfs(processes):
    """
    First-Come, First-Served (FCFS) scheduling algorithm.

    :param processes: A list of dictionaries, each containing:
                      'Process ID', 'Arrival Time', and 'Burst Time'.
    :return: Tuple containing:
             - List of waiting times for each process.
             - Average waiting time.
             - Gantt chart as a list of (Task Label, Duration) tuples.
    """

    # Convert Arrival Time and Burst Time to integers
    for process in processes:
        process['Arrival Time'] = int(process['Arrival Time'])
        process['Burst Time'] = int(process['Burst Time'])

    # Sort the processes by arrival time
    processes.sort(key=lambda x: x['Arrival Time'])

    # Initialize variables
    current_time = 0
    waiting_times = []  # Store waiting time for each process
    gantt_chart = []  # Store Gantt chart entries

    # Calculate waiting time and Gantt chart for each process
    for process in processes:
        # Handle idle time if the CPU is free
        if current_time < process['Arrival Time']:
            idle_time = process['Arrival Time'] - current_time
            gantt_chart.append(('No Task', idle_time))
            current_time = process['Arrival Time']

        # Calculate waiting time for the current process
        waiting_time = current_time - process['Arrival Time']
        waiting_times.append(waiting_time)

        # Add current process to the Gantt chart
        gantt_chart.append((f'Task {process["Process ID"]}', process['Burst Time']))
        current_time += process['Burst Time']

    # Calculate average waiting time
    if len(waiting_times) > 0:
        average_waiting_time = sum(waiting_times) / len(waiting_times)
    else:
        average_waiting_time = 0  # or handle appropriately

    return waiting_times, average_waiting_time, gantt_chart
