import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend for headless servers
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from collections import Counter
import os
import tempfile

# Set up Streamlit page
st.set_page_config(
    page_title="Project Submission Statistics",
    page_icon="📊",
    layout="wide"
)

st.title("ECON1500 Final Project Submission Statistics")
st.markdown("Explore statistics about the final project submissions, including group sizes and student distribution.")
st.markdown("---")

# Since we can't access the actual directory when deployed online,
# we'll use the pre-calculated statistics from our previous analysis

# Function to generate the visualizations based on pre-calculated statistics
def generate_visualizations():
    # Pre-calculated statistics from our analysis
    total_submissions = 49
    total_students = 75
    individual_projects = 35
    group_projects = 14
    
    # Group size distribution
    group_size_counts = {2: 6, 3: 4, 4: 4}
    
    # Calculate derived statistics
    students_in_groups = sum(size * count for size, count in group_size_counts.items())
    percent_in_groups = (students_in_groups / total_students) * 100
    percent_individual = 100 - percent_in_groups
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Submissions", total_submissions)
    with col2:
        st.metric("Total Students", total_students)
    with col3:
        st.metric("Group Projects", group_projects)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Project Types", "Group Sizes", "Student Distribution"])
    
    with tab1:
        st.subheader("Project Types Distribution")
        labels = ['Individual', 'Group']
        sizes = [individual_projects, group_projects]
        colors = ['#ff9999', '#66b3ff']
        
        plt.figure(figsize=(8, 6), dpi=100)
        fig = plt.gcf()
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 14})
        plt.axis('equal')
        st.pyplot(fig)
        
        # Save the chart for download using tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            plt.savefig(tmp_file.name)
        
        # Download option
        with open(tmp_file.name, "rb") as file:
            st.download_button(
                label="Download Chart as PNG",
                data=file.read(),
                file_name="project_types.png",
                mime="image/png",
                key="download_project_types"
            )
    
    with tab2:
        st.subheader("Group Size Distribution")
        sizes = list(group_size_counts.keys())
        counts = list(group_size_counts.values())
        
        plt.figure(figsize=(8, 6), dpi=100)
        fig = plt.gcf()
        plt.bar(sizes, counts, color='#66b3ff')
        plt.xlabel('Group Size', fontsize=12)
        plt.ylabel('Number of Groups', fontsize=12)
        plt.xticks(sizes)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        # Save the chart for download using tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            plt.savefig(tmp_file.name)
        
        # Download option
        with open(tmp_file.name, "rb") as file:
            st.download_button(
                label="Download Chart as PNG",
                data=file.read(),
                file_name="group_sizes.png",
                mime="image/png",
                key="download_group_sizes"
            )
    
    with tab3:
        st.subheader("Student Distribution")
        labels = ['Individual Projects', 'Group Projects']
        student_counts = [individual_projects, students_in_groups]
        colors = ['#ff9999', '#66b3ff']
        
        plt.figure(figsize=(8, 6), dpi=100)
        fig = plt.gcf()
        plt.bar(labels, student_counts, color=colors)
        plt.xlabel('Project Type', fontsize=12)
        plt.ylabel('Number of Students', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add percentage annotations
        for i, count in enumerate(student_counts):
            plt.text(i, count + 0.5, f"{count} ({count/total_students:.1%})", 
                     ha='center', fontsize=12)
        
        st.pyplot(fig)
        
        # Save chart for download
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            plt.savefig(tmp_file.name)
        
        # Download option
        with open(tmp_file.name, "rb") as file:
            st.download_button(
                label="Download Student Distribution Chart",
                data=file.read(),
                file_name="student_distribution.png",
                mime="image/png",
                key="download_student_dist"
            )
    
    # Detailed stats in expandable section
    with st.expander("Detailed Statistics"):
        st.write(f"**Total Submissions:** {total_submissions}")
        st.write(f"**Individual Projects:** {individual_projects}")
        st.write(f"**Group Projects:** {group_projects}")
        
        st.write("\n**Group Size Distribution:**")
        for size, count in sorted(group_size_counts.items()):
            st.write(f"- **{size} members:** {count} projects ({size * count} students)")
        
        st.write(f"\n**Total Students:** {total_students}")
        st.write(f"**Students Working in Groups:** {students_in_groups} ({percent_in_groups:.1f}%)")
        st.write(f"**Students Working Individually:** {individual_projects} ({percent_individual:.1f}%)")

# Generate visualizations
generate_visualizations() 