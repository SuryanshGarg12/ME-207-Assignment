import streamlit as st
import pandas as pd
import random

# Define the Job class
class Job:
    def __init__(self, job_id, processing_time, due_date):
        self.job_id = job_id
        self.processing_time = processing_time
        self.due_date = due_date
        self.flow_time = 0
        self.lateness = 0
        self.slack = 0
        self.criticality = 0

    def calculate_metrics(self, completion_time):
        self.flow_time = completion_time
        self.lateness = max(0, self.flow_time - self.due_date)
        self.slack = self.due_date - self.processing_time
        self.criticality = 1 / (self.flow_time / max(self.due_date, 1))

# Job scheduling functions
def generate_jobs(num_jobs, processing_time_range, due_date_factor_range):
    jobs = []
    total_processing_time = 0

    for i in range(num_jobs):
        processing_time = random.randint(*processing_time_range)
        total_processing_time += processing_time
        job = Job(job_id=i + 1, processing_time=processing_time, due_date=0)
        jobs.append(job)

    for job in jobs:
        job.due_date = random.randint(
            int(total_processing_time * due_date_factor_range[0]),
            int(total_processing_time * due_date_factor_range[1])
        )

    return jobs

def fcfs(jobs):
    return sorted(jobs, key=lambda job: job.job_id)

def spt(jobs):
    return sorted(jobs, key=lambda job: job.processing_time)

def lpt(jobs):
    return sorted(jobs, key=lambda job: -job.processing_time)

def smallest_slack(jobs):
    for i, job in enumerate(jobs):
        job.calculate_metrics(sum(j.processing_time for j in jobs[:i + 1]))
    return sorted(jobs, key=lambda job: job.slack)

def smallest_criticality(jobs):
    for i, job in enumerate(jobs):
        job.calculate_metrics(sum(j.processing_time for j in jobs[:i + 1]))
    return sorted(jobs, key=lambda job: job.criticality)

def random_order(jobs):
    random.shuffle(jobs)
    return jobs

def evaluate_schedule(jobs, scheduling_rule):
    sorted_jobs = scheduling_rule(jobs.copy())
    current_time = 0
    evaluation_results = []

    for job in sorted_jobs:
        current_time += job.processing_time
        job.calculate_metrics(current_time)
        evaluation_results.append(
            {
                "Job ID": job.job_id,
                "Processing Time": job.processing_time,
                "Due Date": job.due_date,
                "Flow Time": job.flow_time,
                "Lateness": job.lateness,
                "Slack": job.slack,
                "Criticality": job.criticality,
            }
        )

    return evaluation_results

# Streamlit App
def main():
    st.set_page_config(page_title="Job Scheduling Tool", layout="wide")
    st.title("Job Scheduling Tool")

    num_jobs = st.number_input("Number of Jobs", min_value=1, step=1, value=5)
    processing_case = st.selectbox("Processing Time Case", ("Case 1", "Case 2", "Case 3"))
    rule = st.selectbox("Sequencing Rule", ("FCFS", "SPT", "LPT", "Smallest Slack", "Smallest Criticality", "Random"))

    if st.button("Run Simulation"):
        processing_range, due_date_factor_range = {
            "Case 1": ((2, 10), (0.3, 0.9)),
            "Case 2": ((2, 50), (0.5, 1.1)),
            "Case 3": ((2, 100), (0.5, 1.1)),
        }[processing_case]

        jobs = generate_jobs(int(num_jobs), processing_range, due_date_factor_range)
        scheduling_rule = {
            "FCFS": fcfs,
            "SPT": spt,
            "LPT": lpt,
            "Smallest Slack": smallest_slack,
            "Smallest Criticality": smallest_criticality,
            "Random": random_order,
        }[rule]

        results = evaluate_schedule(jobs, scheduling_rule)

        st.subheader("Simulation Results")
        
        # Display results in a DataFrame
        results_df = pd.DataFrame(results)
        st.table(results_df)

if __name__ == "__main__":
    main()
