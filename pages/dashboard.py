from shiny import ui
from shinywidgets import output_widget


def dashboard_ui(username: str, finances: dict):
    monthly_income = finances["monthly_income"] + finances["side_income"]

    total_expenses = (
        finances["rent"]
        + finances["groceries"]
        + finances["food_out"]
        + finances["transport"]
        + finances["subscriptions"]
        + finances["utilities"]
        + finances["healthcare"]
        + finances["personal_spending"]
    )

    est_savings = max(monthly_income - total_expenses, 0)

    savings_rate = 0.0
    if monthly_income > 0:
        savings_rate = (est_savings / monthly_income) * 100

    return ui.page_fluid(
        ui.h2("Your FYWISE Outlook", class_="text-center mb-4"),

        # ----- TOP ROW: CHART CARDS (unchanged) -----
        ui.row(
            ui.column(
                4,
                ui.card(
                    ui.card_header("Loan Overview"),
                    # Plotly loan chart
                    output_widget("loan_line"),
                    ui.br(),
                    ui.p(f"Total Balance: ${finances['loan_balance']:,.0f}"),
                    ui.p(f"Monthly Payment: ${finances['monthly_payment']:,.0f}"),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Total Expenses"),
                    # Plotly expenses chart
                    output_widget("expenses_pie"),
                    ui.br(),
                    ui.p(f"Estimated Monthly Expenses: ${total_expenses:,.0f}"),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Income Overview"),
                    # Plotly income chart
                    output_widget("income_bar"),
                    ui.br(),
                    ui.p(f"Total Monthly Income: ${monthly_income:,.0f}"),
                    ui.p(f"Estimated Savings: ${est_savings:,.0f}"),
                ),
            ),
        ),

        # ----- SECOND ROW: VISUAL STAT CARDS (text only, no charts) -----
        ui.br(),
        ui.row(
            ui.column(
                4,
                ui.card(
                    ui.card_header("Money Coming In"),
                    ui.h3(f"${monthly_income:,.0f}", class_="mb-1"),
                    ui.p(
                        "Total monthly take-home from your main job and side income.",
                        class_="text-muted",
                    ),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Money Going Out"),
                    ui.h3(f"${total_expenses:,.0f}", class_="mb-1"),
                    ui.p(
                        "What you currently spend on housing, food, bills, transport, and fun.",
                        class_="text-muted",
                    ),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Room to Breathe"),
                    ui.h3(f"${est_savings:,.0f}", class_="mb-1"),
                    ui.p(
                        f"Approx. {savings_rate:,.1f}% of your income is left after expenses. "
                        "This can go toward savings or extra loan payments.",
                        class_="text-muted",
                    ),
                ),
            ),
        ),
    )
