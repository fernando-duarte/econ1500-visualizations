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
        # Create a pie chart of individual vs. group projects
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        labels = ['Individual Projects', 'Group Projects']
        sizes = [individual_projects, group_projects]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)  # explode the 1st slice
    
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title("Distribution of Project Types", fontsize=14, fontweight='bold')
        st.pyplot(fig1)
        
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
        # Create a bar chart of group sizes
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        group_sizes = sorted(group_size_counts.items())
        x = [f"{size} Members" for size, _ in group_sizes]
        y = [count for _, count in group_sizes]
        
        bars = ax2.bar(x, y, color=['#66b3ff', '#99ff99', '#ffcc99'])
        
        # Add counts above bars
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
        
        plt.title("Group Size Distribution", fontsize=14, fontweight='bold')
        plt.ylabel("Number of Groups")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig2)
        
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
        # Create a pie chart showing percentage of students in groups vs. individual
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        labels = ['Students in Groups', 'Individual Students']
        sizes = [students_in_groups, individual_projects]
        colors = ['#66b3ff', '#ff9999']
        
        ax3.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax3.axis('equal')
        plt.title("Distribution of Students by Project Type", fontsize=14, fontweight='bold')
        st.pyplot(fig3)
        
        # Save the chart for download using tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            plt.savefig(tmp_file.name)
        
        # Download option
        with open(tmp_file.name, "rb") as file:
            st.download_button(
                label="Download Chart as PNG",
                data=file.read(),
                file_name="student_distribution.png",
                mime="image/png",
                key="download_student_dist"
            )
    
        # Detailed breakdown of students by group size
        st.subheader("Student Count by Group Size")
        
        student_counts = {}
        student_counts["Individual"] = individual_projects
        for size, count in group_size_counts.items():
            student_counts[f"{size}-Person Groups"] = size * count
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        x = list(student_counts.keys())
        y = list(student_counts.values())
        
        bars = ax4.bar(x, y, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        
        # Add counts above bars
        for bar in bars:
            height = bar.get_height()
            ax4.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
        
        plt.title("Number of Students by Group Size", fontsize=14, fontweight='bold')
        plt.ylabel("Number of Students")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig4)
        
        # Save the chart for download using tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            plt.savefig(tmp_file.name)
        
        # Download option
        with open(tmp_file.name, "rb") as file:
            st.download_button(
                label="Download Chart as PNG",
                data=file.read(),
                file_name="student_count_by_group.png",
                mime="image/png",
                key="download_student_count"
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