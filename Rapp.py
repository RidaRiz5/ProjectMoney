from shiny import App, ui, reactive, render
from shinywidgets import render_plotly
import plotly.graph_objects as go

import os
from pathlib import Path
from dotenv import load_dotenv
import bcrypt
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    Float,
    MetaData,
    select,
    update,
    insert,
)

# -------------------------------------------------
# DATABASE SETUP (Supabase Postgres)
# -------------------------------------------------

# Load .env (if present)
env_path = Path(__file__).resolve().parent / ".env"
print("Loading .env from:", env_path)
load_dotenv(dotenv_path=env_path)

# Fallback to your provided Supabase URL if env var not set
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:DoogleGocs2025!!!!@db.rltgxygoyptjwbnyvbid.supabase.co:5432/postgres?sslmode=require",
)

print("DATABASE_URL in app.py:", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found. Check your .env file or hard-coded URL.")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    echo=False,
)

metadata = MetaData()

# ----------------- USERS TABLE -------------------
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

# ----------------- FINANCES TABLE ----------------
finances_table = Table(
    "finances",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("monthly_income", Float),
    Column("side_income", Float),
    Column("rent", Float),
    Column("groceries", Float),
    Column("food_out", Float),
    Column("transport", Float),
    Column("subscriptions", Float),
    Column("utilities", Float),
    Column("healthcare", Float),
    Column("personal_spending", Float),
    Column("loan_balance", Float),
    Column("monthly_payment", Float),
    Column("interest_rate", Float),
)

# Create tables if they don't exist yet
metadata.create_all(engine)

# -------------------------------------------------
# DEFAULT FINANCES
# -------------------------------------------------
DEFAULT_FINANCES = {
    "monthly_income": 3200,
    "side_income": 400,
    "rent": 1200,
    "groceries": 300,
    "food_out": 150,
    "transport": 120,
    "subscriptions": 50,
    "utilities": 140,
    "healthcare": 80,
    "personal_spending": 200,
    "loan_balance": 15000,
    "monthly_payment": 250,
    "interest_rate": 4.5,
}

# -------------------------------------------------
# DATABASE HELPERS (LOGIN + FINANCES)
# -------------------------------------------------
def user_exists(username: str) -> bool:
    try:
        with engine.connect() as conn:
            row = (
                conn.execute(
                    select(users_table).where(users_table.c.username == username)
                )
                .mappings()
                .first()
            )
        return row is not None
    except Exception as e:
        print("user_exists ERROR:", e)
        return False


def create_user(username: str, password: str) -> bool:
    if user_exists(username):
        return False

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        with engine.begin() as conn:
            conn.execute(
                users_table.insert().values(username=username, password=hashed)
            )
        # Create default finances row on signup
        save_finances_db(username, DEFAULT_FINANCES.copy())
        return True
    except Exception as e:
        print("create_user ERROR:", e)
        return False


def verify_user(username: str, password: str) -> bool:
    try:
        with engine.connect() as conn:
            row = (
                conn.execute(
                    select(users_table).where(users_table.c.username == username)
                )
                .mappings()
                .first()
            )
    except Exception as e:
        print("verify_user ERROR:", e)
        return False

    if not row:
        return False

    stored_hash = row["password"]
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))


def get_finances(username: str) -> dict:
    """Fetch finances from DB; if none, return defaults and insert them."""
    print("get_finances for:", username)
    try:
        with engine.connect() as conn:
            row = (
                conn.execute(
                    select(finances_table).where(finances_table.c.username == username)
                )
                .mappings()
                .first()
            )
    except Exception as e:
        print("get_finances ERROR (falling back to defaults):", e)
        return DEFAULT_FINANCES.copy()

    if not row:
        # no row yet -> create one with defaults
        data = DEFAULT_FINANCES.copy()
        save_finances_db(username, data)
        return data

    # start with defaults, overwrite any DB values that are not None
    data = DEFAULT_FINANCES.copy()
    for key in data.keys():
        if key in row and row[key] is not None:
            data[key] = row[key]
    return data


def save_finances_db(username: str, data: dict):
    """Insert or update finances row for this user."""
    if not username:
        print("save_finances_db called with empty username – skipping")
        return

    payload = {
        "username": username,
        "monthly_income": float(data.get("monthly_income", 0)),
        "side_income": float(data.get("side_income", 0)),
        "rent": float(data.get("rent", 0)),
        "groceries": float(data.get("groceries", 0)),
        "food_out": float(data.get("food_out", 0)),
        "transport": float(data.get("transport", 0)),
        "subscriptions": float(data.get("subscriptions", 0)),
        "utilities": float(data.get("utilities", 0)),
        "healthcare": float(data.get("healthcare", 0)),
        "personal_spending": float(data.get("personal_spending", 0)),
        "loan_balance": float(data.get("loan_balance", 0)),
        "monthly_payment": float(data.get("monthly_payment", 0)),
        "interest_rate": float(data.get("interest_rate", 0)),
    }

    try:
        with engine.begin() as conn:
            existing = (
                conn.execute(
                    select(finances_table.c.id).where(
                        finances_table.c.username == username
                    )
                )
                .mappings()
                .first()
            )

            if existing:
                conn.execute(
                    update(finances_table)
                    .where(finances_table.c.username == username)
                    .values(**payload)
                )
            else:
                conn.execute(finances_table.insert().values(**payload))

        print("save_finances_db OK for:", username)
    except Exception as e:
        print("save_finances_db ERROR:", e)


# -------------------------------------------------
# IMPORT UI PAGES
# -------------------------------------------------
from pages.login import login_ui
from pages.dashboard import dashboard_ui
from pages.settings import settings_ui
from pages.finance_input import finance_input_ui
from pages.income import income_ui
from pages.expenses import expenses_ui
from pages.loans import loans_ui
from pages.financial_advice import financial_advice_ui
from pages.chatbot import chatbot_ui

# -------------------------------------------------
# CHATBOT SETUP 
# -------------------------------------------------
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are FyWise Assistant — a supportive, concise financial guide.
Keep answers under 100 words.
Stay focused on budgeting, savings, loans, and spending.
Here is the conversation: {context}
Question: {question}
Answer:
"""

llm = OllamaLLM(model="gemma3:1b", base_url="http://localhost:11435")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

# -------------------------------------------------
# MAIN UI 
# -------------------------------------------------
app_ui = ui.page_fluid(
    ui.include_css("assets/style.css"),
    ui.include_css("assets/chatbot.css"),
    ui.h2("FYWISE 💰 Personal Financial Dashboard", class_="app-title text-center mb-3"),
    ui.output_text("status"),
    ui.output_ui("main_ui"),
)

# -------------------------------------------------
# SERVER LOGIC 
# -------------------------------------------------
def server(input, output, session):

    logged_in = reactive.Value(False)
    current_user = reactive.Value("")
    finances = reactive.Value(DEFAULT_FINANCES.copy())
    current_page = reactive.Value("login")
    status_message = reactive.Value("")
    messages = reactive.Value([])

    # ---------- STATUS BAR ----------
    @render.text
    def status():
        return status_message()

    output.status = status

    # ---------- LOGIN ----------
    @reactive.effect
    @reactive.event(input.login_btn)
    def _login():
        u = (input.username() or "").strip()
        p = input.password() or ""

        print("LOGIN attempt for:", u)

        if not u or not p:
            status_message.set("Please enter a username and password.")
            return

        if not verify_user(u, p):
            status_message.set("Invalid username or password.")
            return

        logged_in.set(True)
        current_user.set(u)

        # Load finances from DB
        f = get_finances(u)
        finances.set(f)

        status_message.set(f"Logged in as {u}")
        current_page.set("dashboard")
        print("LOGIN success for:", u)

    # ---------- SIGNUP ----------
    @reactive.effect
    @reactive.event(input.signup_btn)
    def _signup():
        u = (input.username() or "").strip()
        p = input.password() or ""

        if not u or not p:
            status_message.set("Please enter both username and password.")
            return

        if create_user(u, p):
            status_message.set(f"Account created for {u}. You can now log in.")
        else:
            status_message.set("Username already exists.")

    # ---------- LOGOUT ----------
    @reactive.effect
    @reactive.event(input.logout_btn)
    def _logout():
        print("LOGOUT for:", current_user())
        logged_in.set(False)
        current_page.set("login")
        current_user.set("")
        status_message.set("Logged out successfully.")

    # ---------- NAVIGATION ----------
    @reactive.effect
    def nav():
        if not logged_in():
            return

        buttons = {
            "go_dashboard": "dashboard",
            "go_income": "income",
            "go_expenses": "expenses",
            "go_loans": "loans",
            "go_advice": "advice",
            "go_chatbot": "chatbot",
            "go_settings": "settings",
            "go_finance_input": "finance_input",
        }

        for btn, page in buttons.items():
            if hasattr(input, btn) and input[btn]() > 0:
                print("NAV ->", page)
                current_page.set(page)

    # ---------- SAVE FINANCES  ----------
    @reactive.effect
    @reactive.event(input.save_finances)
    def _save_finances():
        newf = {
            "monthly_income": input.monthly_income() or 0,
            "side_income": input.side_income() or 0,
            "rent": input.rent() or 0,
            "groceries": input.groceries() or 0,
            "food_out": input.food_out() or 0,
            "transport": input.transport() or 0,
            "subscriptions": input.subscriptions() or 0,
            "utilities": input.utilities() or 0,
            "healthcare": input.healthcare() or 0,
            "personal_spending": input.personal_spending() or 0,
            "loan_balance": input.loan_balance() or 0,
            "monthly_payment": input.monthly_payment() or 0,
            "interest_rate": input.interest_rate() or 0,
        }
        finances.set(newf)

        save_finances_db(current_user(), newf)

        status_message.set("Financial data saved to your FYWISE account.")
        print("FINANCES saved for:", current_user())

    # ---------- CHARTS ----------
    @render_plotly
    def loan_line():
        f = finances()
        x = [0, 6, 12, 18, 24, 30, 36]
        s = f["loan_balance"]
        y = [s, s * 0.9, s * 0.8, s * 0.65, s * 0.5, s * 0.35, s * 0.2]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers"))
        fig.update_layout(title="Loan Balance Over Time", height=320)
        return fig

    @render_plotly
    def expenses_pie():
        f = finances()
        labels = [
            "Rent",
            "Groceries",
            "Food Out",
            "Transport",
            "Subscriptions",
            "Utilities",
            "Healthcare",
            "Personal",
        ]
        values = [
            f["rent"],
            f["groceries"],
            f["food_out"],
            f["transport"],
            f["subscriptions"],
            f["utilities"],
            f["healthcare"],
            f["personal_spending"],
        ]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title="Monthly Expense Breakdown", height=320)
        return fig

    @render_plotly
    def income_bar():
        f = finances()
        labels = ["Main Job", "Side Income"]
        values = [f["monthly_income"], f["side_income"]]

        fig = go.Figure(data=[go.Bar(x=labels, y=values)])
        fig.update_layout(title="Income Overview", height=320)
        return fig

    output.loan_line = loan_line
    output.expenses_pie = expenses_pie
    output.income_bar = income_bar

    # ---------- CHATBOT ----------
    @render.ui
    def chat_history():
        elems = []
        for m in messages():
            css = "message user" if m["sender"] == "user" else "message bot"
            elems.append(ui.div({"class": css}, m["text"]))
        return elems

    output.chat_history = chat_history

    @reactive.effect
    @reactive.event(input.send_chat)
    def _send_chat():
        msg = (input.chat_input() or "").strip()
        if not msg:
            return

        hist = messages().copy()
        hist.append({"sender": "user", "text": msg})
        messages.set(hist)

        ui.update_text("chat_input", value="")

        ctx = ""
        for m in hist:
            prefix = "User" if m["sender"] == "user" else "AI"
            ctx += f"\n{prefix}: {m['text']}"

        try:
            reply = chain.invoke({"context": ctx, "question": msg})
        except Exception as e:
            reply = f"Error: {e}"

        hist = messages().copy()
        hist.append({"sender": "bot", "text": str(reply)})
        messages.set(hist)

    # ---------- MAIN UI ROUTER ----------
    @render.ui
    def main_ui():
        if not logged_in():
            return login_ui()

        pg = current_page()
        f = finances()

        nav = ui.div(
            ui.row(
                ui.column(
                    12,
                    ui.div(
                        ui.input_action_button("go_dashboard", "Dashboard", class_="btn-nav"),
                        ui.input_action_button("go_income", "Income", class_="btn-nav"),
                        ui.input_action_button("go_expenses", "Expenses", class_="btn-nav"),
                        ui.input_action_button("go_loans", "Loans", class_="btn-nav"),
                        ui.input_action_button("go_advice", "Advice", class_="btn-nav"),
                        ui.input_action_button("go_chatbot", "Chatbot", class_="btn-nav"),
                        ui.input_action_button("go_settings", "Settings", class_="btn-nav"),
                        ui.input_action_button("go_finance_input", "Edit Finances", class_="btn-nav"),
                        class_="text-center",
                    ),
                )
            ),
            ui.hr(),
        )

        if pg == "dashboard":
            body = dashboard_ui(current_user(), f)
        elif pg == "income":
            body = income_ui(f)
        elif pg == "expenses":
            body = expenses_ui(f)
        elif pg == "loans":
            body = loans_ui(f)
        elif pg == "advice":
            body = financial_advice_ui()
        elif pg == "settings":
            body = settings_ui(current_user(), f)
        elif pg == "finance_input":
            body = finance_input_ui(f)
        elif pg == "chatbot":
            body = chatbot_ui()
        else:
            body = ui.h3("Not Found")

        return ui.div(nav, body)

    output.main_ui = main_ui


app = App(app_ui, server)
