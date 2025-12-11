from shiny import ui
from shinywidgets import output_widget


def income_ui(finances: dict):
    total_income = finances["monthly_income"] + finances["side_income"]

    # simple derived views (for display only)
    weekly_income = total_income / 4.33 if total_income > 0 else 0
    daily_income = total_income / 30 if total_income > 0 else 0

    return ui.page_fluid(
        ui.h2("Income Details", class_="text-center mb-3"),

        # ----- TOP ROW: CHART + BREAKDOWN -----
        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Income Chart"),
                    # Plotly income chart (ID unchanged)
                    output_widget("income_bar"),
                ),
            ),
            ui.column(
                6,
                ui.card(
                    ui.card_header("Income Breakdown"),
                    ui.p(f"Main Job Income: ${finances['monthly_income']:,.0f}"),
                    ui.p(f"Side Income: ${finances['side_income']:,.0f}"),
                    ui.hr(),
                    ui.p(f"Total Monthly Income: ${total_income:,.0f}"),
                ),
            ),
        ),

        # ----- SECOND ROW: INCOME SNAPSHOT -----
        ui.br(),
        ui.row(
            ui.column(
                12,
                ui.card(
                    ui.card_header("Income Snapshot"),
                    ui.p(
                        f"Approximate weekly income: ${weekly_income:,.0f}"
                        if weekly_income > 0
                        else "Add income details to see a weekly estimate."
                    ),
                    ui.p(
                        f"Approximate daily income: ${daily_income:,.0f}"
                        if daily_income > 0
                        else "Once you enter income, you'll see a daily estimate here."
                    ),
                    ui.p(
                        "Use these numbers to decide how much you can safely put toward savings or extra loan payments."
                    ),
                ),
            )
        ),
    )
