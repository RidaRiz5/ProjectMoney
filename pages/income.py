from shiny import ui

def income_ui(finances: dict):

    total_income = finances["monthly_income"] + finances["side_income"]

    return ui.page_fluid(
        ui.h2("Income Details", class_="text-center mb-3"),

        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Income Chart"),
                    ui.output_plot("income_bar"),
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
    )