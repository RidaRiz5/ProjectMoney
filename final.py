# python -m shiny run --reload --port 5000 app.py

from shiny import App, ui, reactive, render
from shinywidgets import render_plotly
import bcrypt
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
import plotly.graph_objects as go

# ---------------------------
# DATABASE: USERS
# ---------------------------
engine = create_engine("sqlite:///database.db", echo=False)
metadata = MetaData()

users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)
metadata.create_all(engine)


def user_exists(username: str) -> bool:
    with engine.begin() as conn:
        row = conn.execute(
            select(users_table).where(users_table.c.username == username)
        ).fetchone()
        return row is not None


def create_user(username: str, password: str) -> bool:
    if user_exists(username):
        return False
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    with engine.begin() as conn:
        conn.execute(
            users_table.insert().values(username=username, password=hashed)
        )
    return True


def verify_user(username: str, password: str) -> bool:
    with engine.begin() as conn:
        row = conn.execute(
            select(users_table).where(users_table.c.username == username)
        ).fetchone()
        if row and bcrypt.checkpw(password.encode("utf-8"), row.password.encode("utf-8")):
            return True
    return False


# ---------------------------
# DEFAULT FINANCIAL DATA
# ---------------------------
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
}


# ---------------------------
# IMPORT PAGE UIs
# ---------------------------
from pages.login import login_ui
from pages.dashboard import dashboard_ui
from pages.settings import settings_ui
from pages.finance_input import finance_input_ui
from pages.income import income_ui
from pages.expenses import expenses_ui
from pages.loans import loans_ui
from pages.financial_advice import financial_advice_ui
from pages.chatbot import chatbot_ui


# ---------------------------
# MAIN APP UI
# ---------------------------
app_ui = ui.page_fluid(
    ui.include_css("assets/style.css"),
    ui.h2("FYWISE 💰 Personal Financial Dashboard", class_="app-title text-center mb-3"),
    ui.output_text("status"),
    ui.output_ui("main_ui"),
)


# ---------------------------
# SERVER
# ---------------------------
def server(input, output, session):

    logged_in = reactive.Value(False)
    current_user = reactive.Value("")
    current_page = reactive.Value("login")
    finances = reactive.Value(DEFAULT_FINANCES.copy())
    status_message = reactive.Value("")

    # ---- STATUS BAR ----
    @render.text
    def status():
        return status_message()
    output.status = status

    # ---- LOGIN ----
    @reactive.effect
    @reactive.event(input.login_btn)
    def _login():
        uname = input.username().strip()
        pwd = input.password()
        if verify_user(uname, pwd):
            logged_in.set(True)
            current_user.set(uname)
            current_page.set("dashboard")
            finances.set(DEFAULT_FINANCES.copy())
            status_message.set(f"✅ Logged in as {uname}")
        else:
            status_message.set("❌ Invalid username or password.")

    # ---- SIGNUP ----
    @reactive.effect
    @reactive.event(input.signup_btn)
    def _signup():
        uname = input.username().strip()
        pwd = input.password()
        if not uname or not pwd:
            status_message.set("⚠️ Enter both a username and password.")
            return
        if create_user(uname, pwd):
            status_message.set("✅ Account created! You can now log in.")
        else:
            status_message.set("❌ Username already exists.")

    # ---- LOGOUT ----
    @reactive.effect
    @reactive.event(input.logout_btn)
    def _logout():
        logged_in.set(False)
        current_user.set("")
        current_page.set("login")
        status_message.set("👋 Logged out successfully.")

    # ---- NAVIGATION ----
    @reactive.effect
    def _nav():
        if not logged_in():
            return

        def clicked(name):
            return hasattr(input, name) and input[name]() > 0

        if clicked("go_dashboard"): current_page.set("dashboard")
        if clicked("go_settings"): current_page.set("settings")
        if clicked("go_finance_input"): current_page.set("finance_input")
        if clicked("go_income"): current_page.set("income")
        if clicked("go_expenses"): current_page.set("expenses")
        if clicked("go_loans"): current_page.set("loans")
        if clicked("go_advice"): current_page.set("advice")
        if clicked("go_chatbot"): current_page.set("chatbot")

    # ---- SAVE FINANCES ----
    @reactive.effect
    @reactive.event(input.save_finances)
    def _save_finances():
        if not hasattr(input, "monthly_income"):
            return

        new_data = {k: (getattr(input, k)() or 0) for k in [
            "monthly_income", "side_income",
            "rent", "groceries", "food_out", "transport",
            "subscriptions", "utilities", "healthcare", "personal_spending",
            "loan_balance", "monthly_payment"
        ]}
        finances.set(new_data)
        status_message.set("✅ Financial data updated.")

    # ---- CHATBOT ----
    @render.text
    def chat_reply():
        if not hasattr(input, "chat_input"):
            return ""
        msg = input.chat_input()
        if not msg:
            return ""
        return f"You said: {msg}\n(FYWISE chatbot coming soon ✨)"
    output.chat_reply = chat_reply

    # ---------------------------
    # PLOTLY CHARTS (WORKING NOW)
    # ---------------------------
    @render_plotly
    def loan_line():
        f = finances()
        x = [0, 6, 12, 18, 24, 30, 36]
        start = f["loan_balance"]
        y = [start, start*0.9, start*0.8, start*0.65, start*0.5, start*0.35, start*0.2]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color="#4f46e5", width=3)))
        fig.update_layout(title="Loan Balance Over Time", height=320)
        return fig

    @render_plotly
    def expenses_pie():
        f = finances()
        labels = ["Rent", "Groceries", "Food Out", "Transport", "Subscriptions", "Utilities", "Healthcare", "Personal"]
        values = [
            f["rent"], f["groceries"], f["food_out"], f["transport"],
            f["subscriptions"], f["utilities"], f["healthcare"], f["personal_spending"]
        ]
        fig = go.Figure([go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title="Monthly Expense Breakdown", height=320)
        return fig

    @render_plotly
    def income_bar():
        f = finances()
        fig = go.Figure([
            go.Bar(x=["Main Job", "Side Income"], y=[f["monthly_income"], f["side_income"]],
                   marker_color=["#2563eb", "#10b981"])
        ])
        fig.update_layout(title="Income Overview", height=320)
        return fig

    output.loan_line = loan_line
    output.expenses_pie = expenses_pie
    output.income_bar = income_bar

    # ---- PAGE ROUTER ----
    @render.ui
    def main_ui():
        if not logged_in():
            return login_ui()

        f = finances()
        page = current_page()

        nav = ui.div(
            ui.row(
                ui.column(
                    8,
                    ui.div(
                        ui.input_action_button("go_dashboard", "Dashboard", class_="btn-nav me-1"),
                        ui.input_action_button("go_income", "Income", class_="btn-nav me-1"),
                        ui.input_action_button("go_expenses", "Expenses", class_="btn-nav me-1"),
                        ui.input_action_button("go_loans", "Loans", class_="btn-nav me-1"),
                        ui.input_action_button("go_advice", "Advice", class_="btn-nav me-1"),
                        ui.input_action_button("go_chatbot", "Chatbot", class_="btn-nav me-1"),
                        ui.input_action_button("go_settings", "Settings", class_="btn-nav me-1"),
                    ),
                ),
                ui.column(
                    4,
                    ui.div(
                        ui.span("Logged in as "),
                        ui.strong(current_user()),
                        ui.input_action_button("logout_btn", "Logout", class_="btn-danger ms-3"),
                        class_="text-end"
                    ),
                ),
            ),
            ui.hr(),
        )

        if page == "dashboard":
            body = dashboard_ui(current_user(), f)
        elif page == "settings":
            body = settings_ui(current_user(), f)
        elif page == "finance_input":
            body = finance_input_ui(f)
        elif page == "income":
            body = income_ui(f)
        elif page == "expenses":
            body = expenses_ui(f)
        elif page == "loans":
            body = loans_ui(f)
        elif page == "advice":
            body = financial_advice_ui()
        elif page == "chatbot":
            body = chatbot_ui()
        else:
            body = dashboard_ui(current_user(), f)

        return ui.div(nav, body)

    output.main_ui = main_ui


app = App(app_ui, server)
