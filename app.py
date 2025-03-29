from agents import guide_expert, location_expert, planner_expert
from tasks import location_task, guide_task, planner_task
from crewai import Crew, Process
import streamlit as st
from pyngrok import ngrok

# Ensure ngrok tunnel starts only once
if "ngrok_url" not in st.session_state:
    ngrok.kill()  # Kill any existing tunnels to avoid duplicates
    public_url = ngrok.connect(8501)  # Start a new ngrok tunnel
    st.session_state.ngrok_url = public_url
print((f"Public URL: {st.session_state.ngrok_url}"))


st.title("✈️ Your's Trip Planner Agent")

st.markdown("""
### 💡 **Plan Your Next Trip with AI!**  
""")

from_city = st.text_input("🏡 From Country", "Dubai")
destination_city = st.text_input("✈️ Destination Country", "India")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
interests = st.text_area("🎯 Your Interests (Nature, Food, Adventure) 🍕🏞️🎢", "Adventure & Great Food")



if st.button("🚀 Generate Travel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        st.write("⚙️Preparing Your Plan.....(Just 5-6 Min. 😊)")

        loc_task = location_task(location_expert, from_city, destination_city, date_from, date_to)
        guid_task = guide_task(guide_expert, destination_city, interests, date_from, date_to)
        plan_task = planner_task([loc_task, guid_task], planner_expert, destination_city, interests, date_from, date_to)

        crew = Crew(
            agents=[location_expert, guide_expert, planner_expert],
            tasks=[loc_task, guid_task, plan_task],
            process=Process.sequential,
            full_output=True,
            verbose=True,
        )

        result = crew.kickoff()

        st.subheader("✅ Your AI-Powered Travel Plan")
        st.markdown(result)


        travel_plan_text = str(result)  

        st.download_button(
            label="📥 Download Travel Plan",
            data=travel_plan_text,  
            file_name=f"Travel_Plan_{destination_city}.txt",
            mime="text/plain"
        )
