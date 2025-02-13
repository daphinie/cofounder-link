import streamlit as st
import pymongo
import openai
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from bson.binary import Binary

user = st.secrets["USER"]
password = st.secrets["PASSWORD"]
uri_url = st.secrets["URI_URL"]

uri = f"mongodb+srv://{user}:{password}@{uri_url}/?retryWrites=true&w=majority&appName=Cluster0"

client = pymongo.MongoClient(uri)
db = client["cofounder-link"]
collection = db["answers"]

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Cofounder Link")

st.divider()

st.subheader("Answer these questions and get matched to a potential cofounder")

name = st.text_input("What is your name?")
problem_industry = st.text_area("What problem or industry excites you the most to work on?")
funding = st.text_area("Would you rather bootstrap, raise VC funding, or take another approach?")
impact = st.text_area("How important is financial success vs. impact on society?")
commitment = st.text_area("Are you willing to go full-time on a startup, or are you looking for a side project initially?")
work_environment = st.text_area("What is your preferred work environment? (Remote, hybrid, in-office, co-working spaces)")
ethics = st.text_area("What are your ethical non-negotiables in business?")

def get_embedding(text):
  answer = openai.embeddings.create(
    model="text-embedding-3-small",
    input=text,
  )
  return answer.data[0].embedding

def store_answer(answers, embedding):
  result = collection.insert_one({
    "answers": answers,
    "embedding": Binary(pickle.dumps(embedding))
  })
  return result.inserted_id

def find_match(current_embedding, current_user_id):
  all_answers = list(collection.find())
  similarities = []

  for document in all_answers:
    if document['_id'] == current_user_id:
      continue
    stored_embedding = pickle.loads(document['embedding'])
    similarity = cosine_similarity([current_embedding], [stored_embedding])[0][0]
    similarities.append((similarity, document['answers']))
  
  similarities.sort(reverse=True, key=lambda x: x[0])

  return similarities[0][1] if similarities else None

if st.button("Submit"):
  if name and problem_industry and funding and impact and commitment and work_environment and ethics:
    answers = {
      "name": name,
      "problem_industry": problem_industry,
      "funding": funding,
      "impact": impact,
      "commitment": commitment,
      "work_environment": work_environment,
      "ethics": ethics
    }

    answers_text = " ".join(answers.values())
    actual_embedding = get_embedding(answers_text)
    
    current_user_id = store_answer(answers, actual_embedding)

    match = find_match(actual_embedding, current_user_id)

    if match:
      top_match, top_answer = match[0]
      st.success(f"Match found! Your potential cofounder: {match}")
    else:
      st.warning("You are the first person who's completed this survey so far.")
else:
  st.warning("Please answer all questions")