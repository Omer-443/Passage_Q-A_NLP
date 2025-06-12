from transformers import pipeline
from config import QA_MODEL_NAME

qa_model = pipeline("question-answering", model=QA_MODEL_NAME)

def answer_question(question, chunk):
    return qa_model(question=question, context=chunk)['answer']