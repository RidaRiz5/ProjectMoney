from shiny import ui

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

    return ui.page_fluid(
        ui.h2("Your FYWISE Outlook", class_="text-center mb-4"),

        ui.row(
            ui.column(
                4,
                ui.card(
                    ui.card_header("Loan Overview"),
                    ui.output_plot("loan_line"),
                    ui.br(),
                    ui.p(f"Total Balance: ${finances['loan_balance']:,.0f}"),
                    ui.p(f"Monthly Payment: ${finances['monthly_payment']:,.0f}"),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Total Expenses"),
                    ui.output_plot("expenses_pie"),
                    ui.br(),
                    ui.p(f"Estimated Monthly Expenses: ${total_expenses:,.0f}"),
                ),
            ),
            ui.column(
                4,
                ui.card(
                    ui.card_header("Income Overview"),
                    ui.output_plot("income_bar"),
                    ui.br(),
                    ui.p(f"Total Monthly Income: ${monthly_income:,.0f}"),
                    ui.p(f"Estimated Savings: ${est_savings:,.0f}"),
                ),
            ),
        ),
    )