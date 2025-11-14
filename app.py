# Needs .env, requirements.txt to run

# python -m pip install shiny pandas plotly bcrypt sqlalchemy shinywidgets jinja2 psycopg2-binary python-dotenv
# python -m shiny run --reload app.py

from dotenv import load_dotenv
import os
from pathlib import Path
from shiny import App, ui, reactive, render
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px
import bcrypt
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select


# --- Load .env explicitly ---
env_path = Path(__file__).resolve().parent / ".env"
print("Loading .env from:", env_path)
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL (runtime):", DATABASE_URL)  # Debug print


if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found. Check your .env path!")

# --- Database setup ---
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    echo=False
)

metadata = MetaData()


# Users table
users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

# Create the table if it doesn't exist yet
metadata.create_all(engine)

# ============================================================
# Database Helper Functions
# ============================================================
def user_exists(username):
    with engine.begin() as conn:
        result = conn.execute(
            select(users_table).where(users_table.c.username == username)
        ).fetchone()
        return result is not None

def create_user(username, password):
    if user_exists(username):
        return False

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with engine.begin() as conn:
        conn.execute(
            users_table.insert().values(
                username=username,
                password=hashed
            )
        )
    return True

def verify_user(username, password):
    with engine.begin() as conn:
        user = conn.execute(
            select(users_table).where(users_table.c.username == username)
        ).fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return True

    return False

def sample_data(username):
    return pd.DataFrame({
        "Investment": ["Stocks", "Crypto", "Bonds", "Real Estate"],
        "Gain/Loss ($)": [1500, -200, 400, 2500],
        "User": username,
    })

# ============================================================
# UI Layout
# ============================================================
app_ui = ui.page_fluid(
    ui.h2("💰 Personal Financial Dashboard"),
    ui.output_text("status"),
    ui.output_ui("main_ui"),
)

# ============================================================
# Server Logic
# ============================================================
def server(input, output, session):

    logged_in = reactive.Value(False)
    current_user = reactive.Value(None)
    status_message = reactive.Value("")

    # -------------------------
    # SIGN UP
    # -------------------------
    @reactive.effect
    @reactive.event(input.signup_btn)
    def signup():
        try:
            uname = input.username().strip()
            pword = input.password()

            if not uname or not pword:
                status_message.set("⚠️ Please enter both username and password.")
                return

            if create_user(uname, pword):
                status_message.set(f"✅ Account created for {uname}. You can now log in.")
            else:
                status_message.set("❌ Username already exists.")
        except Exception as e:
            print("🔥 Signup error:", e)
            status_message.set(f"⚠️ Signup failed: {e}")

    # -------------------------
    # LOGIN
    # -------------------------
    @reactive.effect
    @reactive.event(input.login_btn)
    def login():
        uname = input.username().strip()
        pword = input.password()

        if verify_user(uname, pword):
            logged_in.set(True)
            current_user.set(uname)
            status_message.set(f"✅ Logged in as {uname}.")
        else:
            status_message.set("❌ Invalid credentials.")

    # -------------------------
    # LOGOUT
    # -------------------------
    @reactive.effect
    @reactive.event(input.logout_btn)
    def logout():
        logged_in.set(False)
        current_user.set(None)
        status_message.set("👋 Logged out successfully.")

    # -------------------------
    # STATUS DISPLAY
    # -------------------------
    @render.text
    def status():
        return status_message()

    output.status = status

    # -------------------------
    # MAIN UI SWITCH
    # -------------------------
    @render.ui
    def main_ui():
        if not logged_in():
            return ui.card(
                ui.h3("Create an Account or Log In"),
                ui.input_text("username", "Username"),
                ui.input_password("password", "Password"),
                ui.row(
                    ui.input_action_button("login_btn", "Login", class_="btn-primary"),
                    ui.input_action_button("signup_btn", "Sign Up", class_="btn-success"),
                ),
            )

        else:
            return ui.card(
                ui.h3(f"📊 Dashboard - Welcome {current_user()}!"),
                ui.output_table("dashboard_table"),
                ui.output_plot("dashboard_chart"),
                ui.input_action_button("logout_btn", "Logout", class_="btn-danger"),
            )

    # -------------------------
    # DASHBOARD TABLE
    # -------------------------
    @render.table
    def dashboard_table():
        if logged_in():
            return sample_data(current_user())
        return pd.DataFrame()

    # -------------------------
    # DASHBOARD CHART
    # -------------------------
    @render_plotly
    def dashboard_chart():
        if logged_in():
            df = sample_data(current_user())
            fig = px.bar(
                df,
                x="Investment",
                y="Gain/Loss ($)",
                color="Gain/Loss ($)",
                title="Financial Gains/Losses"
            )
            return fig
        return None

    output.main_ui = main_ui
    output.dashboard_table = dashboard_table
    output.dashboard_chart = dashboard_chart

# ============================================================
# App
# ============================================================
app = App(app_ui, server)

# Run with:
# python -m shiny run --reload app.py


# http://127.0.0.1:8000







