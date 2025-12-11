from shiny import ui
from shinywidgets import output_widget


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

    # simple 50/30/20-style grouping (for display only)
    needs = (
        finances["rent"]
        + finances["groceries"]
        + finances["transport"]
        + finances["utilities"]
        + finances["healthcare"]
    )
    wants = (
        finances["food_out"]
        + finances["subscriptions"]
        + finances["personal_spending"]
    )
    other = max(total_expenses - needs - wants, 0)

    needs_pct = wants_pct = other_pct = 0.0
    if total_expenses > 0:
        needs_pct = needs / total_expenses * 100
        wants_pct = wants / total_expenses * 100
        other_pct = other / total_expenses * 100

    return ui.page_fluid(
        ui.h2("Expenses Overview", class_="text-center mb-3"),

        # ----- TOP ROW: CHART + BREAKDOWN -----
        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Expense Breakdown"),
                    # Plotly expenses chart (ID unchanged)
                    output_widget("expenses_pie"),
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

        # ----- SECOND ROW: 50/30/20-STYLE SUMMARY -----
        ui.br(),
        ui.row(
            ui.column(
                12,
                ui.card(
                    ui.card_header("Spending Snapshot"),
                    ui.p(
                        "This grouping uses a simple version of the 50/30/20 rule just to show where your money tends to go."
                    ),
                    ui.p(f"Essential needs (rent, groceries, transport, utilities, healthcare): "
                         f"${needs:,.0f} ({needs_pct:,.1f}% of your expenses)"),
                    ui.p(f"Wants (eating out, subscriptions, personal fun): "
                         f"${wants:,.0f} ({wants_pct:,.1f}% of your expenses)"),
                    ui.p(f"Other / ungrouped: ${other:,.0f} ({other_pct:,.1f}% of your expenses)"),
                ),
            )
        ),
    )
