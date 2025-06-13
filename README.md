# 🧠 Contextual Passage-Based Question Answering System

A powerful, user-friendly web application built with **Streamlit** that answers questions based on user-uploaded or pasted passages. This system uses a modular NLP architecture with contextual memory, chunked embeddings, and semantic search — ideal for educational tools, customer support, document assistants, and more.

---

## 🚀 Features

- 🔐 Login / Signup Authentication
- 📄 Upload or paste context passages (`.txt`)
- 🧱 Modular NLP pipeline
- 🧠 Chat memory (per user session)
- 🔍 Chunked semantic retrieval using embeddings
- 🤖 Answers from best-matching passage chunk
- 🧼 Clear session and logout functionality
- 🧑‍💻 Simple, clean Streamlit interface

---

## 📁 Project Structure

```

contextual-qa-app/
├── main.py                     # Streamlit app entry point
├── modules/
│   ├── auth.py                 # Login / Signup management
│   ├── chunker.py              # Text chunking logic
│   ├── embedder.py             # Sentence embedding using SBERT
│   ├── retriever.py            # Retrieve best matching chunk
│   ├── answerer.py             # Extracts answer from text
│   ├── memory.py               # Chat memory (Q\&A history)
|── users.json                  #user database(Created on first use)
├── requirements.txt
└── README.md                   # Project README (you are here)

````

---

## ⚙️ Installation

### 1. Clone this repository

```bash
git clone https://github.com/Omer-443/Passage_Q-A_NLP.git
cd Passage_Q-A_NLP
````

### 2. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually install essentials:

```bash
pip install streamlit torch sentence-transformers bcrypt
```

---

## ▶️ Running the App

Start the Streamlit app:

```bash
streamlit run main.py
```

## 🧠 How It Works

1. **Login or Sign Up** (User authentication handled in `auth.py`)
2. **Paste or Upload** a text passage
3. The passage is **chunked** into small sections
4. Each chunk is **embedded** into a semantic vector using `sentence-transformers`
5. On user question:

   * The question is embedded
   * Similarity is computed to find the best-matching chunk
6. The **best chunk** is passed to the **answer generator**
7. The **answer is displayed** with optional context view
8. The interaction is **saved to memory** for the session

---

## 🧠 Chat Memory

* Stores recent questions and answers
* Displayed in the sidebar
* Memory resets if session is cleared or restarted

---

## 🔐 Authentication

* New users can sign up securely
* Passwords are hashed with bcrypt
* User data is stored in `data/users.db`
* Includes login/logout functionality

---

## 📦 Sample `.txt` Inputs

Try passages from:

* News articles
* Wikipedia excerpts
* PDFs or lecture notes converted to `.txt`
* Custom study material

---

## 📦 Requirements

### `requirements.txt`

```
streamlit>=1.25
torch
sentence-transformers
bcrypt
```

---

## 📝 License

This project is licensed under the **MIT License**.
Feel free to use, modify, and share!

---

## 📌 Future Improvements

* Add per-user persistent memory (file/DB)
* Token limit slider for better chunking control
* Support for PDF and DOCX files
* Use LLMs for more advanced answering
* Multilingual support
* Streamlit Cloud or Hugging Face Spaces deployment

---

## 🙋‍♂️ Author

**Your Name**
📧 [omerfaisal701@gmail.com](mailto:omerfaisal701@gmail.com)
🌐 GitHub: [@Omer-443](https://github.com/Omer-443)

---

## 📞 Contact

Have feedback or questions?
Open an issue or email me — happy to help!


