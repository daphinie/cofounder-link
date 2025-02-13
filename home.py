import streamlit as st
import pymongo
import openai
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from bson.binary import Binary

user = st.secrets["USER"]
password = st.secrets["PASSWORD"]
uri_url = st.secrets["URI_URL"]

uri = 'mongodb+srv://{user}:{password}>@{uri_url}/?retryWrites=true&w=majority&appName=Cluster0'

client = pymongo.MongoClient(uri)
db = client["cofounder-link"]
collection = db["answers"]

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Cofounder Link")

st.divider()

st.subheader("Answer these questions and get matched to a potential cofounder")

name = st.text_input["What is your name?"]
problem_industry = st.text_area("What problem or industry excites you the most to work on?")
skills = st.text_area("What are your primary technical or business skills? (e.g., coding, product design, marketing, finance, sales)")
cofounder_skills = st.text_area("What specific skills, expertise, or knowledge do you want your ideal co-founder to bring to the table?")
funding = st.text_area("Would you rather bootstrap, raise VC funding, or take another approach?")
impact = st.text_area("How important is financial success vs. impact on society?")
commitment = st.text_area("Are you willing to go full-time on a startup, or are you looking for a side project initially?")
work_environment = st.text_area("What is your preferred work environment? (Remote, hybrid, in-office, co-working spaces)")
ethics = st.text_area("What are your ethical non-negotiables in business?")

def get_embedding(text):
  answer = client.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
  })
  return answer.data[0].embedding

def store_answer(answer, embedding):
  result = collection.insert_one({
    "answers": answer,
    "embedding": Binary(pickle.dumps(embedding))
  })
  return result.inserted_id

def find_match(current_user_id, current_embedding):
  all_answers = list(collection.find())
  similarities = []

  for document in all_answers:
    if document['_id'] == current_user_id:
      continue
    stored_embedding = pickle.loads(document["embedding"])
    similarity = cosine_similarity([current_embedding], [stored_embedding])[0][0]
    similarities.append(similarity, document["responses"])
  
  similarities.sort(reverse=True, key=lambda x:x[0])

  return similarities[0][1] if similarities else None

if st.button("Submit"):
  # TODO: recommendation function
  st.success("Match found!")
else:
  st.warning("Please answer all questions")