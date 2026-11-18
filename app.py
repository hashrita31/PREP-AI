import json
import random
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="Prep AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto",  # collapses automatically on phones
)

# ------------------------------------------------------------------- styling
# Colors come from .streamlit/config.toml so light/dark mode both work.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    h1, h2, h3, h4, p, label, li, button, input, textarea {
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
    }
    .block-container {
        max-width: 1040px;
        padding: 2.5rem 1.5rem 4rem;
    }
    h1 { font-size: 1.8rem !important; font-weight: 600 !important; letter-spacing: -0.01em; }
    h2, h3 { font-weight: 600 !important; }

    .page-sub { opacity: .7; margin: -0.5rem 0 1.5rem; line-height: 1.55; max-width: 62ch; }

    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 10px;
        padding: .9rem 1.1rem;
    }
    [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 10px; }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 8px;
        font-weight: 500;
        padding: .5rem 1.25rem;
    }
    [data-testid="stSidebar"] { border-right: 1px solid rgba(128,128,128,.2); }
    #MainMenu, footer { visibility: hidden; }

    .hero {
        display: flex; flex-wrap: wrap; align-items: center; gap: 1.5rem;
        padding: 1.75rem 2rem; border-radius: 14px; color: #fff;
        background: linear-gradient(135deg, #2F6F6B 0%, #3E8F89 100%);
        margin-bottom: 1.25rem;
    }
    .hero-text { flex: 1 1 280px; }
    .hero-title { font-size: 1.35rem; font-weight: 600; line-height: 1.2; margin: 0 0 .6rem; }
    .hero-sub { opacity: .9; line-height: 1.55; margin: 0; max-width: 46ch; }
    .hero-art { flex: 0 1 230px; width: 230px; max-width: 100%; margin: 0 auto; }
    .brand { display: flex; align-items: center; gap: .6rem; }
    .brand-name { font-size: 1.25rem; font-weight: 600; letter-spacing: -0.01em; }
    .brand-big .brand-name { font-size: 2.1rem; }
    .hero .brand { margin-bottom: 1rem; }
    .card-icon { font-size: 1.9rem; line-height: 1; margin-bottom: .35rem; }
    .tip-box {
        border-left: 3px solid #2F6F6B; padding: .6rem 1rem;
        background: rgba(47,111,107,.08); border-radius: 0 8px 8px 0;
    }

    @media (max-width: 640px) {
        .hero { padding: 1.25rem; }
        .hero-title { font-size: 1.15rem; }
        .block-container { padding: 1.25rem .85rem 3rem; }
        h1 { font-size: 1.45rem !important; }
        .stButton > button, .stFormSubmitButton > button { width: 100%; }
    }
    @media (prefers-reduced-motion: reduce) {
        * { transition: none !important; animation: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------- data
TOPICS = ["Arrays", "Linked List", "Stack", "Queue", "DBMS", "OS"]

ROADMAPS = {
    "Arrays": ["Array basics", "Sliding window", "Prefix sum", "LeetCode practice"],
    "Linked List": ["Linked list basics", "Reverse a linked list", "Fast & slow pointers", "Interview problems"],
    "Stack": ["Stack basics", "Monotonic stack", "Expression evaluation", "Advanced problems"],
    "Queue": ["Queue basics", "Circular queue", "Priority queue", "Graph applications"],
    "DBMS": ["SQL basics", "Joins", "Normalization", "Transactions & indexing"],
    "OS": ["Processes & threads", "Scheduling", "Deadlock", "Memory management"],
}

FALLBACK_QUESTIONS = {
    "Arrays": ["Find the second largest element in an array.", "Rotate an array by k positions.", "Find two numbers that add up to a target.", "Explain Kadane's algorithm."],
    "Linked List": ["Reverse a linked list.", "Detect a cycle in a linked list.", "Find the middle node.", "Merge two sorted linked lists."],
    "Stack": ["Check for balanced parentheses.", "Implement a stack using queues.", "What is a monotonic stack?", "Evaluate a postfix expression."],
    "Queue": ["Implement a queue using stacks.", "What is a circular queue?", "Explain a priority queue.", "Where is BFS using a queue applied?"],
    "DBMS": ["What is normalization?", "Explain the types of joins.", "What are ACID properties?", "What is an index and when does it help?"],
    "OS": ["Difference between a process and a thread?", "What is deadlock and how is it prevented?", "Explain paging vs segmentation.", "Name common CPU scheduling algorithms."],
}


@st.cache_data
def load_questions():
    """Returns (question_bank, loaded_from_file)."""
    path = Path("questions.json")
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), True
        except (json.JSONDecodeError, OSError):
            pass
    return FALLBACK_QUESTIONS, False


@st.cache_resource
def readiness_model():
    X = [[20], [35], [45], [55], [65], [75], [85], [95]]
    y = ["Low", "Low", "Medium", "Medium", "Good", "Good", "Excellent", "Excellent"]
    return DecisionTreeClassifier(random_state=42).fit(X, y)


# --------------------------------------------------------------------- state
st.session_state.setdefault("scores", {})
st.session_state.setdefault("student_name", "")
st.session_state.setdefault("role", "")
st.session_state.setdefault("branch", "")
st.session_state.setdefault("year", "")


def brand_html(big: bool = False) -> str:
    cls = "brand brand-big" if big else "brand"
    return f'<div class="{cls}"><span class="brand-name">Prep AI</span></div>'


def go(page: str):
    """Button callback: jump to another page."""
    st.session_state.nav = page


def header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.markdown(f'<p class="page-sub">{subtitle}</p>', unsafe_allow_html=True)


def need_assessment():
    st.info("Complete the Skill Assessment first to see this page.")


def weak_and_strong(scores):
    weak = [k for k, v in scores.items() if v < 50]
    strong = [k for k, v in scores.items() if v >= 75]
    return weak, strong


# ------------------------------------------------------------------- sidebar
PAGES = [
    "Home",
    "Student Profile",
    "Skill Assessment",
    "Dashboard",
    "Roadmap",
    "Interview Questions",
    "Progress Tracker",
]

with st.sidebar:
    st.markdown(brand_html(), unsafe_allow_html=True)
    st.write("")
    if st.session_state.student_name:
        st.caption(f"{st.session_state.student_name} · {st.session_state.role or 'No role set'}")
    st.session_state.setdefault("nav", "Home")
    menu = st.radio("Navigation", PAGES, key="nav", label_visibility="collapsed")

# ---------------------------------------------------------------------- Home
if menu == "Home":
    name = st.session_state.student_name
    scores = st.session_state.scores
    title = f"Welcome back, {name}" if name else "Get ready for your next technical interview"

    # Hero banner with an inline illustration (no image files needed)
    st.markdown(
        f"""<div class="hero">
<div class="hero-text">
{brand_html(big=True)}
<p class="hero-title">{title}</p>
<p class="hero-sub">Rate your skills, find weak topics, follow a focused plan and practise real questions.</p>
</div>
<svg class="hero-art" viewBox="0 0 230 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Chart with rising bars and a target">
<rect x="10" y="20" width="150" height="120" rx="10" fill="#fff" fill-opacity=".14"/>
<rect x="28" y="96" width="20" height="30" rx="4" fill="#fff" fill-opacity=".55"/>
<rect x="58" y="78" width="20" height="48" rx="4" fill="#fff" fill-opacity=".7"/>
<rect x="88" y="58" width="20" height="68" rx="4" fill="#fff" fill-opacity=".85"/>
<rect x="118" y="38" width="20" height="88" rx="4" fill="#fff"/>
<circle cx="180" cy="52" r="34" fill="#fff" fill-opacity=".16"/>
<circle cx="180" cy="52" r="23" fill="none" stroke="#fff" stroke-width="3" stroke-opacity=".8"/>
<circle cx="180" cy="52" r="11" fill="none" stroke="#fff" stroke-width="3"/>
<circle cx="180" cy="52" r="3.5" fill="#fff"/>
<circle cx="176" cy="122" r="22" fill="#fff" fill-opacity=".9"/>
<path d="M165 122 l8 8 l15 -17" fill="none" stroke="#2F6F6B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
</div>""",
        unsafe_allow_html=True,
    )

    # Next-step button and setup progress
    done = [bool(name), bool(scores), bool(st.session_state.get("generated"))]
    if not name:
        next_page, next_label = "Student Profile", "Set up your profile"
    elif not scores:
        next_page, next_label = "Skill Assessment", "Rate your skills"
    elif not done[2]:
        next_page, next_label = "Interview Questions", "Practise questions"
    else:
        next_page, next_label = "Dashboard", "View your dashboard"

    left, right = st.columns([2, 3], vertical_alignment="center")
    with left:
        st.button(f"{next_label}  ➜", type="primary", on_click=go, args=(next_page,), use_container_width=True)
    with right:
        st.progress(sum(done) / 3, text=f"Getting started: {sum(done)} of 3 steps done")
        st.caption(
            f"{'✅' if done[0] else '⬜'} Profile   "
            f"{'✅' if done[1] else '⬜'} Skill assessment   "
            f"{'✅' if done[2] else '⬜'} Practice questions"
        )

    # Live snapshot once the assessment exists
    if scores:
        avg = sum(scores.values()) / len(scores)
        weak, strong = weak_and_strong(scores)
        m1, m2, m3 = st.columns(3)
        m1.metric("📈 Average score", f"{avg:.0f}%")
        m2.metric("⚠️ Weak topics", len(weak))
        m3.metric("💪 Strong topics", len(strong))

    # Clickable feature cards
    st.subheader("Where do you want to go?")
    features = [
        ("👤", "Student Profile", "Set your role, branch and year.", "Student Profile"),
        ("🧠", "Skill Assessment", "Score yourself on six core topics.", "Skill Assessment"),
        ("📊", "Dashboard", "See weak and strong topics at a glance.", "Dashboard"),
        ("🗺️", "Roadmap", "Get a 4-week plan for weak topics.", "Roadmap"),
        ("💡", "Interview Questions", "Practise by topic and difficulty.", "Interview Questions"),
        ("🎯", "Progress Tracker", "Check your interview readiness.", "Progress Tracker"),
    ]
    cols = st.columns(3)
    for i, (icon, label, text, page) in enumerate(features):
        with cols[i % 3].container(border=True):
            st.markdown(f'<div class="card-icon">{icon}</div>', unsafe_allow_html=True)
            st.markdown(f"**{label}**")
            st.caption(text)
            st.button("Open", key=f"open_{page}", on_click=go, args=(page,), use_container_width=True)

    # Rotating tip
    tips = [
        "Explain your approach out loud before you write any code.",
        "Start with a brute-force idea, then improve it. Interviewers like seeing the steps.",
        "Practise one weak topic every day instead of many topics once a week.",
        "State the time and space complexity of every solution you write.",
        "Ask clarifying questions about input size and edge cases first.",
    ]
    st.session_state.setdefault("tip_i", 0)
    st.subheader("Tip")
    t1, t2 = st.columns([4, 1], vertical_alignment="center")
    t1.markdown(f'<div class="tip-box">💬 {tips[st.session_state.tip_i % len(tips)]}</div>', unsafe_allow_html=True)
    if t2.button("Next tip", use_container_width=True):
        st.session_state.tip_i += 1
        st.rerun()

# ------------------------------------------------------------------- Profile
elif menu == "Student Profile":
    header("Student Profile", "This is used to personalise your plan. It stays in this session only.")

    roles = ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Analyst", "ML Engineer"]
    branches = ["BCA", "BTech", "MCA", "BSc(IT)", "MSc(IT)"]
    years = ["1st Year", "2nd Year", "3rd Year", "Final Year"]

    def idx(options, value):
        return options.index(value) if value in options else 0

    with st.form("profile_form"):
        name = st.text_input("Name", value=st.session_state.student_name)
        role = st.selectbox("Preferred role", roles, index=idx(roles, st.session_state.role))
        c1, c2 = st.columns(2)
        branch = c1.selectbox("Branch", branches, index=idx(branches, st.session_state.branch))
        year = c2.selectbox("Year", years, index=idx(years, st.session_state.year))
        saved = st.form_submit_button("Save profile", type="primary")

    if saved:
        if not name.strip():
            st.error("Enter your name to save the profile.")
        else:
            st.session_state.update(student_name=name.strip(), role=role, branch=branch, year=year)
            st.success("Profile saved.")

# ---------------------------------------------------------------- Assessment
elif menu == "Skill Assessment":
    header("Skill Assessment", "Rate yourself from 0 to 100 on each topic. Be honest: it makes the plan better.")

    previous = st.session_state.scores
    with st.form("assessment_form"):
        left, right = st.columns(2)
        values = {}
        for i, topic in enumerate(TOPICS):
            col = left if i % 2 == 0 else right
            values[topic] = col.slider(topic, 0, 100, previous.get(topic, 50))
        submitted = st.form_submit_button("Analyse skills", type="primary")

    if submitted:
        st.session_state.scores = values
        st.success("Assessment saved. Open the Dashboard to see your results.")

# ----------------------------------------------------------------- Dashboard
elif menu == "Dashboard":
    header("Dashboard")

    scores = st.session_state.scores
    if not scores:
        need_assessment()
    else:
        weak, strong = weak_and_strong(scores)
        avg = sum(scores.values()) / len(scores)

        c1, c2, c3 = st.columns(3)
        c1.metric("Average score", f"{avg:.0f}%")
        c2.metric("Weak topics", len(weak))
        c3.metric("Strong topics", len(strong))

        st.subheader("Topic performance")
        df = pd.DataFrame({"Topic": list(scores.keys()), "Score": list(scores.values())}).set_index("Topic")
        st.bar_chart(df, height=280, use_container_width=True)

        left, right = st.columns(2)
        with left.container(border=True):
            st.markdown("**Needs work** (below 50)")
            if weak:
                for t in weak:
                    st.write(f"• {t} — {scores[t]}")
            else:
                st.caption("No weak topics. Nice.")
        with right.container(border=True):
            st.markdown("**Strong** (75 and above)")
            if strong:
                for t in strong:
                    st.write(f"• {t} — {scores[t]}")
            else:
                st.caption("No strong topics yet.")

# ------------------------------------------------------------------- Roadmap
elif menu == "Roadmap":
    header("Learning Roadmap", "A four-week plan for every topic you scored below 50.")

    scores = st.session_state.scores
    if not scores:
        need_assessment()
    else:
        weak, _ = weak_and_strong(scores)
        if not weak:
            st.success("No weak topics. Keep practising advanced problems.")
        else:
            for topic in weak:
                with st.expander(f"{topic} · current score {scores[topic]}", expanded=len(weak) == 1):
                    for week, item in enumerate(ROADMAPS[topic], start=1):
                        st.write(f"**Week {week}** — {item}")

# ----------------------------------------------------------------- Questions
elif menu == "Interview Questions":
    header("Interview Questions", "Pick a topic and difficulty, then practise out loud before checking your answer.")

    bank, from_file = load_questions()
    if not from_file:
        st.caption("`questions.json` not found, so built-in sample questions are being used.")

    c1, c2 = st.columns(2)
    topic = c1.selectbox("Topic", list(bank.keys()))
    difficulty = c2.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate questions", type="primary"):
        pool = bank[topic]
        # supports {"Arrays": [...]} and {"Arrays": {"Easy": [...], ...}}
        if isinstance(pool, dict):
            pool = pool.get(difficulty, [])
        if not pool:
            st.warning(f"No {difficulty.lower()} questions for {topic} yet.")
        else:
            st.session_state.generated = random.sample(pool, min(3, len(pool)))
            st.session_state.generated_label = f"{difficulty} · {topic}"

    if st.session_state.get("generated"):
        st.subheader(st.session_state.generated_label)
        for i, q in enumerate(st.session_state.generated, start=1):
            with st.container(border=True):
                st.markdown(f"**Q{i}.** {q}")

# ------------------------------------------------------------------ Progress
elif menu == "Progress Tracker":
    header("Progress Tracker")

    scores = st.session_state.scores
    if not scores:
        need_assessment()
    else:
        avg = sum(scores.values()) / len(scores)

        st.subheader("Current vs target")
        for topic, score in scores.items():
            st.caption(f"{topic} — {score} / 100")
            st.progress(score / 100)

        st.subheader("Interview readiness")
        level = readiness_model().predict([[avg]])[0]
        messages = {
            "Low": ("error", "You need strong preparation before placements."),
            "Medium": ("warning", "You are improving but still need practice."),
            "Good": ("info", "Good preparation level. Keep practising."),
            "Excellent": ("success", "Excellent preparation level."),
        }
        kind, text = messages[level]

        m1, m2 = st.columns(2)
        m1.metric("Readiness level", level)
        m2.metric("Average score", f"{avg:.0f}%")
        getattr(st, kind)(text)