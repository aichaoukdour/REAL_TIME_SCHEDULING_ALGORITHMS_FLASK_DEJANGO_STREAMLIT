import plotly.figure_factory as ff

def gantt_chart(c):
    # Create a list to store the Gantt chart data
    gantt_data = []

    # Set a color for all tasks (e.g., blue)
    task_color = 'rgb(0, 0, 255)'

    # Iterate through the gantt_representation and create Gantt chart data
    current_time_slot = 0
    for task, duration in c:
        if task == 'Task No Task' or task == 'No Task':
            current_time_slot += duration
            continue  # Skip Task No Task
        gantt_data.append(
            dict(Task=task, Start=current_time_slot, Finish=current_time_slot + duration, Color=task_color))
        current_time_slot += duration

    # Create a Gantt chart figure
    fig = ff.create_gantt(
        gantt_data,
        show_colorbar=True,
        showgrid_y=True,
        showgrid_x=True,
        index_col='Task',
        group_tasks=True,
    )

    # Update the layout of the chart
    fig.update_layout(
        title_text='Gantt Chart Representation',
        xaxis_title='Time Slots',
        yaxis_title='Tasks',
        xaxis_type='linear',
        xaxis=dict(range=[0, current_time_slot]),  # Set the range of x-axis
    )

    # Return the HTML representation of the figure
    return fig.to_html(full_html=False)
