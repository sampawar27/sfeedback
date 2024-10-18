import streamlit as st
import pandas as pd
import os

csv_file = 'student_feedback1.csv'
feedback_dict = {}

user_credentials = {
    "DS": "ds",
    "MP": "mp",
    "SE": "se",
    "DM": "dm"
}
def checkFeedBack(selected_unit):
    subject_map = {
        "DS": "Data Structure",
        "MP": "Microprocessor",
        "SE": "Software Engineering",
        "DM": "District Mathematics"
    }

    subject = subject_map.get(st.session_state.username, "General")
    if os.path.isfile(csv_file):
        existing_feedback_df = pd.read_csv(csv_file)
    else:
        existing_feedback_df = pd.DataFrame(columns=["Subject", "Units", "Rating", "Feedback"])

    user_feedback = existing_feedback_df[(existing_feedback_df["Subject"] == subject) & 
                                         (existing_feedback_df["Units"] == selected_unit)]
    
    st.sidebar.subheader(f"{subject} Feedback for {selected_unit}")

    if not user_feedback.empty:
        st.sidebar.write("Feedback in table format:")
        st.sidebar.dataframe(user_feedback)  # Display the filtered feedback as a scrollable table
    else:
        st.sidebar.write("No feedback available.")
def display_subject_average_ratings(selected_unit):
    subject_map = {
        "DS": "Data Structure",
        "MP": "Microprocessor",
        "SE": "Software Engineering",
        "DM": "District Mathematics"
    }
    subject = subject_map.get(st.session_state.get('username', "General"))

    if os.path.isfile(csv_file):
        feedback_df = pd.read_csv(csv_file)

        if not feedback_df.empty:
            subject_feedback = feedback_df[(feedback_df["Subject"] == subject) &
                                           (feedback_df["Units"] == selected_unit)]

            if not subject_feedback.empty:
                st.subheader(f"Your Subject's Ratings for {selected_unit}")

                avg_rating = subject_feedback["Rating"].mean()

                if avg_rating >= 4:
                    color = 'green'  # Green for rating >= 4
                    performance = "Best"
                elif avg_rating >= 2.5:
                    color = 'yellow'  # Yellow for rating between 2.5 and 4
                    performance = "Better"
                else:
                    color = 'red'  # Red for rating < 2.5
                    performance = "Poor"

                st.subheader(f"Average Rating for {subject} - {selected_unit} (★)")
                stars = "★" * int(avg_rating) + "☆" * (5 - int(avg_rating))  

                st.markdown(f"<span style='color:{color}; font-size:24px;'>{stars}</span>", unsafe_allow_html=True)
                st.write(f"Average Rating: {avg_rating:.2f}/5")
                st.write(f"Feedback Performance: {performance} for {subject} in {selected_unit}.")
            else:
                st.write(f"No feedback available for {subject} in {selected_unit}.")
        else:
            st.write("No feedback data available.")
    else:
        st.write("No feedback file found.")

st.title("Student Feedback Form")

st.sidebar.header("Login")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

units = ["Unit 1","Unit 2","Unit 3","Unit 4","Unit 5", "Unit 6"]

if not st.session_state.logged_in:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    selectunit  = st.sidebar.selectbox("Select Subject", units)
    
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if username in user_credentials and user_credentials[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in successfully as {username}!")
            checkFeedBack(selectunit)  
        else:
            st.error("Invalid username or password.")
st.subheader("Student Feedback")
subjects = ["Data Structure", "Microprocessor", "Software Engineering", "District Mathematics"]
units = ["Unit 1","Unit 2","Unit 3","Unit 4","Unit 5", "Unit 6"]
with st.form(key='feedback_form'):
    subject = st.selectbox("Select Subject", subjects)
    units  = st.selectbox("Select Subject", units)

    rating = st.slider("Rate the subject (1-5)", 1.0, 5.0)
    feedback = st.text_area("Your Feedback")
    submit_button = st.form_submit_button(label='Submit Feedback')
    if submit_button:
        feedback_dict[subject] = {
            "Subject": subject,
            "Units": units,
            "Rating": rating,
            "Feedback": feedback
        }

        feedback_df = pd.DataFrame([feedback_dict[subject]])  

        if os.path.isfile(csv_file):
            feedback_df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            feedback_df.to_csv(csv_file, mode='w', header=True, index=False)

        st.success("Thank you for your feedback!")
display_subject_average_ratings(selectunit)
