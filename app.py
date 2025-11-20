# python -m shiny run --reload --port 5000 app.py

from shiny import App, ui, reactive, render
from shinywidgets import render_plotly
import bcrypt
import plotly.graph_objects as go
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
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
}

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
# MAIN UI
# -------------------------------------------------
app_ui = ui.page_fluid(
    ui.include_css("assets/style.css"),
    ui.h2("FYWISE 💰 Personal Financial Dashboard", class_="app-title text-center mb-3"),
    ui.output_text("status"),
    ui.output_ui("main_ui"),
)


# -------------------------------------------------
# SERVER
# -------------------------------------------------
def server(input, output, session):

    logged_in = reactive.Value(False)
    current_user = reactive.Value("")
    finances = reactive.Value(DEFAULT_FINANCES.copy())
    current_page = reactive.Value("login")
    status_message = reactive.Value("")

    # STATUS BAR
    @render.text
    def status():
        return status_message()

    output.status = status

    # LOGIN
    @reactive.effect
    @reactive.event(input.login_btn)
    def _login():
        u = input.username().strip()
        p = input.password()
        if verify_user(u, p):
            logged_in.set(True)
            current_user.set(u)
            current_page.set("dashboard")
            finances.set(DEFAULT_FINANCES.copy())
            status_message.set(f"✅ Logged in as {u}")
        else:
            status_message.set("❌ Invalid username or password.")

    # SIGNUP
    @reactive.effect
    @reactive.event(input.signup_btn)
    def _signup():
        u = input.username().strip()
        p = input.password()
        if not u or not p:
            status_message.set("⚠️ Please enter both username and password.")
            return
        if create_user(u, p):
            status_message.set("✅ Account created! You can now log in.")
        else:
            status_message.set("❌ Username already exists.")

    # LOGOUT
    @reactive.effect
    @reactive.event(input.logout_btn)
    def _logout():
        logged_in.set(False)
        current_page.set("login")
        current_user.set("")
        status_message.set("👋 Logged out successfully.")

    # NAVIGATION
    @reactive.effect
    def nav():
        if not logged_in():
            return

        def pressed(btn_id: str) -> bool:
            return hasattr(input, btn_id) and input[btn_id]() > 0

        if pressed("go_dashboard"):
            current_page.set("dashboard")
        if pressed("go_income"):
            current_page.set("income")
        if pressed("go_expenses"):
            current_page.set("expenses")
        if pressed("go_loans"):
            current_page.set("loans")
        if pressed("go_advice"):
            current_page.set("advice")
        if pressed("go_chatbot"):
            current_page.set("chatbot")
        if pressed("go_settings"):
            current_page.set("settings")
        if pressed("go_finance_input"):
            current_page.set("finance_input")

    # SAVE FINANCES
    @reactive.effect
    @reactive.event(input.save_finances)
    def _save_finances():
        # Only run if the finance_input page has been shown at least once
        if not hasattr(input, "rent"):
            return

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
        }
        finances.set(newf)
        status_message.set("✅ Financial data updated for this session.")

    # -------------------------------
    # CHARTS (WORKING VERSION)
    # -------------------------------
    @render_plotly
    def loan_line():
        f = finances()
        x = [0, 6, 12, 18, 24, 30, 36]
        s = f["loan_balance"]
        y = [s, s * 0.9, s * 0.8, s * 0.65, s * 0.5, s * 0.35, s * 0.2]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                line=dict(color="#4f46e5", width=3),
            )
        )
        fig.update_layout(
            title="Loan Balance Over Time",
            height=320,
            margin=dict(l=30, r=20, t=40, b=40),
        )
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
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                )
            ]
        )
        fig.update_layout(
            title="Monthly Expense Breakdown",
            height=320,
            margin=dict(l=20, r=20, t=40, b=40),
        )
        return fig

    @render_plotly
    def income_bar():
        f = finances()
        labels = ["Main Job", "Side Income"]
        values = [f["monthly_income"], f["side_income"]]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=labels,
                    y=values,
                    marker_color=["#2563eb", "#10b981"],
                )
            ]
        )
        fig.update_layout(
            title="Income Overview",
            height=320,
            margin=dict(l=30, r=20, t=40, b=40),
        )
        return fig

    output.loan_line = loan_line
    output.expenses_pie = expenses_pie
    output.income_bar = income_bar

    # ---- CHATBOT REPLY ----
    @render.text
    def chat_reply():
        if not hasattr(input, "chat_input"):
            return ""
        msg = input.chat_input()
        if not msg:
            return ""
        return f"You said: {msg}\n(FYWISE chatbot coming soon ✨)"

    output.chat_reply = chat_reply

    # MAIN UI ROUTER
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
                        class_="text-center"
                    )
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