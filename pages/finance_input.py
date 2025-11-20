from shiny import ui

def finance_input_ui(finances: dict):

    return ui.page_fluid(
        ui.h2("Edit Your Financial Inputs", class_="text-center mb-3"),

        ui.card(
            ui.card_header("Income"),
            ui.input_numeric("monthly_income", "Main Job Income (per month)", finances["monthly_income"]),
            ui.input_numeric("side_income", "Side Income (per month)", finances["side_income"]),
        ),

        ui.br(),

        ui.card(
            ui.card_header("Basic Expenses"),
            ui.input_numeric("rent", "Rent / Housing", finances["rent"]),
            ui.input_numeric("groceries", "Groceries", finances["groceries"]),
            ui.input_numeric("transport", "Transportation", finances["transport"]),
        ),

        ui.br(),

        ui.card(
            ui.card_header("Expanded Expenses"),
            ui.input_numeric("food_out", "Eating Out", finances["food_out"]),
            ui.input_numeric("subscriptions", "Subscriptions", finances["subscriptions"]),
            ui.input_numeric("utilities", "Utilities", finances["utilities"]),
            ui.input_numeric("healthcare", "Healthcare / Medical", finances["healthcare"]),
            ui.input_numeric("personal_spending", "Personal / Fun Money", finances["personal_spending"]),
        ),

        ui.br(),

        ui.card(
            ui.card_header("Loans"),
            ui.input_numeric("loan_balance", "Loan Balance", finances["loan_balance"]),
            ui.input_numeric("monthly_payment", "Monthly Payment", finances["monthly_payment"]),
        ),

        ui.br(),
        ui.input_action_button("save_finances", "Save Financial Data", class_="btn-success"),
        ui.p("These changes will update your dashboard for this session.", class_="mt-2 text-muted"),
    )