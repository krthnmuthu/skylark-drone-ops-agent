import streamlit as st
from logic import assign_mission

st.set_page_config(page_title="Skylark Drone Ops Agent")

st.title("🚁 Skylark Drone Operations Coordinator AI")
st.write("Ask me to assign pilots and drones to missions.")

# Input box
user_input = st.text_input(
    "Enter your request (example: Assign mission PRJ002):"
)

# Button
if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a command.")
    else:
        # Very simple intent extraction
        words = user_input.split()
        project_id = None

        for word in words:
            if word.upper().startswith("PRJ"):
                project_id = word.upper()

        if not project_id:
            st.error("❌ Please specify a valid project ID (e.g., PRJ002).")
        else:
            result = assign_mission(project_id)
            st.success(result)
