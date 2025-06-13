import streamlit as st
from modules import chunker, embedder, retriever, answerer, memory, auth

st.set_page_config(page_title="🧠 Context QA System", layout="wide")

# ---------------- LOGIN PAGE ------------------
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid username or password")

# ---------------- SIGNUP PAGE ------------------
def signup_page():
    st.title("📝 Sign Up")

    def is_password_strong(password):
        import re
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False
    if "otp_verified" not in st.session_state:
        st.session_state["otp_verified"] = False

    if not st.session_state["otp_sent"]:
        with st.form("send_otp_form"):
            new_username = st.text_input("New Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            send_otp = st.form_submit_button("Send OTP")
            if send_otp:
                if not new_email:
                    st.error("❌ Please enter an email address")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif not is_password_strong(new_password):
                    st.error("❌ Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")
                else:
                    if auth.request_otp(new_email):
                        st.session_state["otp_sent"] = True
                        st.session_state["email"] = new_email
                        st.session_state["username"] = new_username
                        st.session_state["password"] = new_password
                        st.success("✅ OTP sent to your email")
                    else:
                        st.error("❌ Failed to send OTP. Please try again later.")
    elif st.session_state["otp_sent"] and not st.session_state["otp_verified"]:
        with st.form("verify_otp_form"):
            otp_input = st.text_input("Enter OTP")
            verify_otp = st.form_submit_button("Verify OTP")
            if verify_otp:
                verified, msg = auth.verify_otp(st.session_state["email"], otp_input)
                if verified:
                    st.session_state["otp_verified"] = True
                    st.success("✅ OTP verified. You can now sign up.")
                else:
                    st.error(f"❌ {msg}")
    else:
        with st.form("signup_form"):
            sign_up = st.form_submit_button("Sign Up")
            if sign_up:
                if auth.add_user(st.session_state["username"], st.session_state["email"], st.session_state["password"]):
                    st.success("✅ User created successfully! You are now logged in.")
                    st.session_state.logged_in = True
                    st.session_state.username = st.session_state["username"]
                    st.session_state["otp_sent"] = False
                    st.session_state["otp_verified"] = False
                    st.session_state.pop("email", None)
                    st.session_state.pop("username", None)
                    st.session_state.pop("password", None)
                else:
                    st.error("❌ Username or email already exists")

def forgotten_password_page():
    st.title("🔑 Forgot Password")
    email = st.text_input("Enter your registered email")
    otp_sent = st.session_state.get("fp_otp_sent", False)
    otp_verified = st.session_state.get("fp_otp_verified", False)
    otp_input = st.text_input("Enter OTP") if otp_sent and not otp_verified else ""
    new_password = st.text_input("New Password", type="password") if otp_verified else ""
    confirm_password = st.text_input("Confirm Password", type="password") if otp_verified else ""

    def is_password_strong(password):
        import re
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    if not otp_sent:
        if st.button("Send OTP"):
            if not email:
                st.error("❌ Please enter your email")
            else:
                if auth.request_otp(email):
                    st.session_state["fp_otp_sent"] = True
                    st.success("✅ OTP sent to your email")
                else:
                    st.error("❌ Failed to send OTP. Please try again later.")
    elif otp_sent and not otp_verified:
        if st.button("Verify OTP"):
            verified, msg = auth.verify_otp(email, otp_input)
            if verified:
                st.session_state["fp_otp_verified"] = True
                st.success("✅ OTP verified. You can now reset your password.")
            else:
                st.error(f"❌ {msg}")
    else:
        if st.button("Reset Password"):
            if new_password != confirm_password:
                st.error("❌ Passwords do not match")
            elif not is_password_strong(new_password):
                st.error("❌ Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")
            elif auth.reset_password(email, new_password):
                st.success("✅ Password reset successfully. You can now login.")
                st.session_state.pop("fp_otp_sent", None)
                st.session_state.pop("fp_otp_verified", None)
            else:
                st.error("❌ Failed to reset password. Please try again.")

# ---------------- ROUTER ------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if st.session_state.logged_in:
        main_app()
    else:
        page = st.sidebar.radio("Select Page", ["Login", "Sign Up", "Forgot Password"])
        if page == "Login":
            login_page()
        elif page == "Sign Up":
            signup_page()
        else:
            forgotten_password_page()


# ---------------- MAIN QA APP ------------------
def main_app():
    st.title("🧠 Passage-Based Question Answering")

    if "memory" not in st.session_state:
        st.session_state.memory = memory.ContextualMemory()

    with st.sidebar:
        st.header("🔧 Settings")

        pasted_text = st.text_area("📋 Paste context passage here")
        uploaded_file = st.file_uploader("📄 Upload context file (.txt only)", type="txt")
        
        if st.button("Clear Session"):
            keys_to_clear = ["chunks", "embeddings", "memory"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("🧹 Session cleared!")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("🔒 Logged out")

        if st.session_state.logged_in:
            st.markdown("---")
            st.subheader("⚠️ Danger Zone")
            if "username" in st.session_state:
                if st.button("Delete Account"):
                    confirm = st.text_input("Type DELETE to confirm account deletion")
                    if confirm == "DELETE":
                        if auth.delete_user(st.session_state.username):
                            st.success("🗑️ Account deleted successfully.")
                            st.session_state.logged_in = False
                            st.session_state.username = None
                            # Clear session memory
                            keys_to_clear = ["chunks", "embeddings", "memory"]
                            for key in keys_to_clear:
                                if key in st.session_state:
                                    del st.session_state[key]
                        else:
                            st.error("❌ Failed to delete account.")
                    elif confirm and confirm != "DELETE":
                        st.error("❌ Confirmation text incorrect. Please type DELETE to confirm.")

    context = None
    if pasted_text:
        context = pasted_text
    elif uploaded_file:
        context = uploaded_file.read().decode("utf-8")

    if context:
        chunks = chunker.chunk_text(context)
        embeddings = embedder.get_embeddings(chunks)
        st.session_state["chunks"] = chunks
        st.session_state["embeddings"] = embeddings
        st.success(f"✅ Loaded {len(chunks)} context chunks.")

    question = st.text_input("💬 Ask a question:")
    if question:
        if "chunks" in st.session_state and "embeddings" in st.session_state:
            chunks = st.session_state["chunks"]
            embeddings = st.session_state["embeddings"]
            best_chunk = retriever.find_best_chunk(question, chunks, embeddings)
            answer = answerer.answer_question(question, best_chunk)

            st.markdown(f"### ✅ Answer: {answer}")
            with st.expander("📌 Context Used"):
                st.write(best_chunk)

            if "memory" in st.session_state:
                st.session_state.memory.add_turn(question, answer, best_chunk)
        else:
            st.warning("⚠️ Please upload or paste a context passage first.")

    with st.sidebar:
        st.subheader("🧠 Chat History")
        if "memory" in st.session_state:
            for q, a in reversed(st.session_state.memory.get_history()):
                st.markdown(f"**Q:** {q}\n\n**A:** {a}")

# ---------------- ROUTER ------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if st.session_state.logged_in:
        main_app()
    else:
        page = st.sidebar.radio("Select Page", ["Login", "Sign Up"])
        if page == "Login":
            login_page()
        else:
            signup_page()

if __name__ == "__main__":
    main()
