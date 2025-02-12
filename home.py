import streamlit as st

st.title("Cofounder Link")

st.divider()

st.subheader("Answer these questions and get matched to a potential cofounder")

problem_industry = st.text_input("What problem or industry excites you the most to work on?")
skills = st.text_input("What are your primary technical or business skills? (e.g., coding, product design, marketing, finance, sales)")
cofounder_skills = st.text_input("What specific skills, expertise, or knowledge do you want your ideal co-founder to bring to the table?")
funding = st.text_input("Would you rather bootstrap, raise VC funding, or take another approach?")
impact = st.text_input("How important is financial success vs. impact on society?")
commitment = st.text_input("Are you willing to go full-time on a startup, or are you looking for a side project initially?")
work_environment = st.text_input("What is your preferred work environment? (Remote, hybrid, in-office, co-working spaces)")
ethics = st.text_input("What are your ethical non-negotiables in business?")

if st.button("Submit"):
  # TODO: recommendation function
  st.success("Match found!")
else:
  st.warning("Please answer all questions")