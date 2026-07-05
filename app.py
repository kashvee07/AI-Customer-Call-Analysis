import os
import streamlit as st

from pipeline import analyze_customer_call
from utils.search import search_transcript
from utils.report import generate_report

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Customer Call Analyzer",
    page_icon="🎧",
    layout="wide"
)

# -------------------------------------------------------
# LOAD CSS
# -------------------------------------------------------

if os.path.exists("styles.css"):
    with open("styles.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "file_path" not in st.session_state:
    st.session_state.file_path = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🎧 AI Customer Call Analyzer</h1>

<p>
Analyze customer support conversations using Speech Recognition,
Sentiment Analysis and Named Entity Recognition.
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# UPLOAD SECTION
# -------------------------------------------------------

st.markdown("## 📂 Upload Audio")

uploaded_file = st.file_uploader(
    "",
    type=["mp3","wav","m4a"]
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(path,"wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state.file_path = path
    st.session_state.file_name = uploaded_file.name

    st.success("File Uploaded Successfully")

    st.write(f"**Filename:** {uploaded_file.name}")

if st.session_state.file_path:

    if st.button(
        "🚀 Analyze Call",
        use_container_width=True
    ):

        with st.spinner("Analyzing..."):

            st.session_state.result = analyze_customer_call(
                st.session_state.file_path
            )

# -------------------------------------------------------
# RESULTS
# -------------------------------------------------------

if st.session_state.result:

    result = st.session_state.result

    if result["success"]:

        sentiment = result["sentiment"]

        st.markdown("<br>", unsafe_allow_html=True)

        # --------------------------------------------

        col1,col2,col3 = st.columns(3)

        with col1:

            if sentiment["label"].lower()=="positive":
                emoji="🟢"

            elif sentiment["label"].lower()=="negative":
                emoji="🔴"

            else:
                emoji="🟡"

            st.markdown(f"""
            <div class="card">

            <h3>😊 Sentiment</h3>

            <h2>{emoji} {sentiment['label'].title()}</h2>

            <p>Confidence<br>
            <b>{sentiment['score']*100:.2f}%</b></p>

            </div>
            """,unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="card">

            <h3>📌 Entities</h3>

            <h1>{len(result["entities"])}</h1>

            <p>Detected</p>

            </div>
            """,unsafe_allow_html=True)

        with col3:

            words=len(result["transcript"].split())

            st.markdown(f"""
            <div class="card">

            <h3>📄 Transcript</h3>

            <h1>{words}</h1>

            <p>Words</p>

            </div>
            """,unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # --------------------------------------------

        st.markdown("""
        <div class="section-title">
        📝 Transcript
        </div>
        """,unsafe_allow_html=True)

        st.markdown(f"""
        <div class="transcript">

        {result["transcript"]}

        </div>
        """,unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # --------------------------------------------

        st.markdown("""
        <div class="section-title">
        📌 Named Entities
        </div>
        """,unsafe_allow_html=True)

        icon_map={
            "PERSON":"👤",
            "ORG":"🏢",
            "DATE":"📅",
            "PRODUCT":"📦",
            "GPE":"📍",
            "TIME":"⏰",
            "MONEY":"💰"
        }

        if result["entities"]:

            cols=st.columns(3)

            for i,entity in enumerate(result["entities"]):

                icon=icon_map.get(
                    entity["label"],
                    "🏷️"
                )

                with cols[i%3]:

                    st.markdown(f"""
                    <div class="entity">

                    {icon} {entity["text"]}

                    </div>
                    """,unsafe_allow_html=True)

        else:

            st.info("No entities detected.")

        st.markdown("<br>",unsafe_allow_html=True)

        # --------------------------------------------

        st.markdown("""
        <div class="section-title">
        🔍 Search Transcript
        </div>
        """,unsafe_allow_html=True)

        c1,c2=st.columns([5,1])

        with c1:

            query=st.text_input(
                "",
                placeholder="Search keyword..."
            )

        with c2:

            search=st.button("Search")

        if search:

            matches=search_transcript(
                result["transcript"],
                query
            )

            if matches:

                st.success(
                    f"{len(matches)} match(es) found."
                )

                for m in matches:

                    st.markdown(f"""
                    <div class="match">

                    {m}

                    </div>
                    """,unsafe_allow_html=True)

            else:

                st.warning("No matches found.")

        st.markdown("<br>",unsafe_allow_html=True)

        report=generate_report(result)

        st.download_button(
            "⬇ Download Analysis Report",
            report,
            "customer_support_report.txt",
            "text/plain",
            use_container_width=True
        )

    else:

        st.error(result["error"])

st.markdown("""
<hr>

<center>

Built with ❤️ using Whisper • Transformers • spaCy • Streamlit

</center>
""",unsafe_allow_html=True)