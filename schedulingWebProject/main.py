import streamlit as st
from FCFS.FCFS import fcfs
from LLF.llf_runner import llf_function
from EDF.edf_runner import edf_function
from SJF.SJF_without_preemption import sjf_without_preemption
from preemptif_SJF.SJF_with_preemption import sjf_with_preemption
from RM.rm_runner import rm_runner
from DM.dm_runner import dm_runner
from gantt_chart_drawer import gantt_chart

# Apply custom CSS styles for a cleaner and more modern look
st.markdown(
    """
    <style>
    /* Global style for the app */
    .main {
        background-color: #add8e6; /* Light blue background */
        padding: 2rem;
        color:#34495e;
        font-family: 'Arial', sans-serif;
    }

    /* Header */
    .css-1v3fvcr h1 {
        color:#34495e;
        text-align: center;
        color: #F5F5DC; /* Dark green */
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-transform: uppercase;
    }

    /* Sidebar */
   .stSidebar {
     background-color: #F5F5DC;/* Green gradient */
        color:#34495e;
        padding: 1rem;
        border-radius: 8px;
    }
    .stSidebar {
     background-color: #F5F5DCe;
     
     }
    
    .stSidebar selectbox {
        color: #34495e;
        background-color: #004d40; /* Dark green */
        border: none;
        padding: 0.8rem;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stSidebar selectbox:hover {
        background-color: #00332d; /* Even darker green */
    }

    /* Button styles */
    .stButton>button {
        background-color: #34495e; /* Green button */
        color:#ffff;
        border-radius: 8px;
        padding: 12px 20px;
        border: none;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }

    /* Tables */
    .st-table {
        background-color: #ffffff; /* White table background */
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
       color:#34495e;
        overflow-x: auto;
    }

    /* Input fields */
    .stTextInput, .stNumberInput {
        padding: 10px;
        color:#34495e;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    
    .stTextInput input, .stNumberInput input {
        color:#34495e;
        background-color: #e9f7f1; /* Light green input fields */
    }

    /* Title and Subheading styles */
    .st-subheader {
       color:#34495e; /* Dark green */
        font-weight: bold;
    }

    /* Custom styling for the Gantt chart */
    .gantt-chart {
        color:#34495e;
        margin-top: 20px;
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 3rem;
    }

    /* Make the Gantt chart more visually appealing */
    .gantt-chart rect {
        fill: #4CAF50; /* Green bars in the Gantt chart */
        stroke: white;
        stroke-width: 1px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        font-size: 1rem;
        color: #00796b; /* Dark green footer text */
    }
    </style>
    """, unsafe_allow_html=True
)

# Your main function and logic here
def fcfsOrSJF_page(algorithm):
    st.subheader(f"{algorithm} Scheduling Algorithm STREAMLIT", anchor="algorithm-title",)
     # Initialize session state for data if not already done
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "Task": [],
            "Burst Time": [],
            "Arrival Time": [],
            "Deadline": [],  # Ensure 'Deadline' is initialized
            "Period": []
        }

    if "data" not in st.session_state:
        st.session_state["data"] = {"Task": [], "Burst Time": [], "Arrival Time": []}

    data = st.session_state["data"]

    with st.form("Input Data", clear_on_submit=True):
        st.table(data)
        col1, col2 = st.columns(2)
        with col1:
            new_burst_time = st.number_input("Enter Burst Time:", min_value=1, step=1)
        with col2:
            new_arrival_time = st.number_input("Enter Arrival Time:", min_value=0, step=1)

        add_button = st.form_submit_button("Add Task")
        if add_button:
            data["Task"].append("T" + str(len(st.session_state.data["Arrival Time"]) + 1))
            data["Burst Time"].append(new_burst_time)
            data["Arrival Time"].append(new_arrival_time)
            st.session_state["data"] = data
            st.table(data)

    if st.button(f"Run {algorithm}", use_container_width=True):
        tasks = st.session_state.data["Task"]
        burst_times = st.session_state.data["Burst Time"]
        arrival_times = st.session_state.data["Arrival Time"]

        processes = [{"Process ID": i + 1, "Task": tasks[i], "Arrival Time": arrival_times[i],
                      "Burst Time": burst_times[i]} for i in range(len(burst_times))]

        if algorithm == "FCFS":
            a, b, c = fcfs(processes)
        elif algorithm == "SJF Without Preemption":
            a, b, c = sjf_without_preemption(processes)
        else:
            a, b, c = sjf_with_preemption(processes)

        st.subheader("Response:")
        st.text(f"Waiting Times: {a}, Average Waiting Time: {b}")
        st.markdown('<div class="gantt-chart">', unsafe_allow_html=True)
        gantt_chart(c)
        st.markdown('</div>', unsafe_allow_html=True)


def dm_rm_edf_llf_page(algorithm):
    st.subheader(f"{algorithm} Scheduling Algorithm", anchor="algorithm-title")
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "Task": [], "Arrival Time": [], "Burst Time": [], "Deadline": [], "Period": []}

    data = st.session_state["data"]

    with st.form("Input Data", clear_on_submit=True):
        st.table(data)
        col1, col2 = st.columns(2)
        with col1:
            new_arrival_time = st.number_input("Enter Arrival Time:", min_value=0, step=1)
        with col2:
            new_burst_time = st.number_input("Enter Burst Time:", min_value=1, step=1)

        new_deadline = st.number_input("Enter Deadline:", min_value=1, step=1)
        new_period = st.number_input("Enter Period:", min_value=1, step=1)

        add_button = st.form_submit_button("Add Task")
        if add_button:
            data["Task"].append("T" + str(len(st.session_state.data["Arrival Time"]) + 1))
            data["Arrival Time"].append(new_arrival_time)
            data["Burst Time"].append(new_burst_time)
            data["Deadline"].append(new_deadline)
            data["Period"].append(new_period)
            st.session_state["data"] = data
            st.table(data)

    if st.button(f"Run {algorithm}", use_container_width=True):
        tasks = st.session_state.data["Task"]
        arrival_times = st.session_state.data["Arrival Time"]
        burst_times = st.session_state.data["Burst Time"]
        deadlines = st.session_state.data["Deadline"]
        periods = st.session_state.data["Period"]

        processes = [{"Process ID": i + 1, "Task": tasks[i], "Arrival Time": arrival_times[i],
                      "Burst Time": burst_times[i], "Deadline": deadlines[i], "Period": periods[i]}
                     for i in range(len(burst_times))]

        if algorithm == "RM":
            b, c = rm_runner(processes)
        elif algorithm == "DM":
            b, c = dm_runner(processes)
        elif algorithm == "EDF":
            b, c = edf_function(processes)
        elif algorithm == "LLF":
            b, c = llf_function(processes)

        st.subheader("Response:")
        st.text(f"CPU Occupation: {b}")
        st.markdown('<div class="gantt-chart">', unsafe_allow_html=True)
        gantt_chart(c)
        st.markdown('</div>', unsafe_allow_html=True)


# App Logic
def run_app():
    st.title("Real-Time Scheduling Algorithms")
    st.markdown("Select the algorithm and enter the necessary task parameters.")

    algorithm = st.sidebar.radio("Select Algorithm", ["FCFS", "SJF Without Preemption", "SJF With Preemption",
                                                    "RM", "DM", "EDF", "LLF"])

    if algorithm in ["FCFS", "SJF Without Preemption", "SJF With Preemption"]:
        fcfsOrSJF_page(algorithm)
    else:
        dm_rm_edf_llf_page(algorithm)


if __name__ == "__main__":
    run_app()
