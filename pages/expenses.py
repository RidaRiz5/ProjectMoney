from shiny import ui

def expenses_ui(finances: dict):

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

    return ui.page_fluid(
        ui.h2("Expenses Overview", class_="text-center mb-3"),

        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Expense Breakdown"),
                    ui.output_plot("expenses_pie"),
                ),
            ),
            ui.column(
                6,
                ui.card(
                    ui.card_header("Expense Details"),
                    ui.p(f"Rent / Housing: ${finances['rent']:,.0f}"),
                    ui.p(f"Groceries: ${finances['groceries']:,.0f}"),
                    ui.p(f"Eating Out: ${finances['food_out']:,.0f}"),
                    ui.p(f"Transportation: ${finances['transport']:,.0f}"),
                    ui.p(f"Subscriptions: ${finances['subscriptions']:,.0f}"),
                    ui.p(f"Utilities: ${finances['utilities']:,.0f}"),
                    ui.p(f"Healthcare: ${finances['healthcare']:,.0f}"),
                    ui.p(f"Personal / Fun: ${finances['personal_spending']:,.0f}"),
                    ui.hr(),
                    ui.p(f"Total Monthly Expenses: ${total_expenses:,.0f}"),
                ),
            ),
        ),
    )