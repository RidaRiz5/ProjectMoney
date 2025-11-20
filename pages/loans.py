from shiny import ui

def loans_ui(finances: dict):

    return ui.page_fluid(
        ui.h2("Loan Overview", class_="text-center mb-3"),

        ui.row(
            ui.column(
                7,
                ui.card(
                    ui.card_header("Loan Balance Trend"),
                    ui.output_plot("loan_line"),
                ),
            ),
            ui.column(
                5,
                ui.card(
                    ui.card_header("Loan Details"),
                    ui.p(f"Current Balance: ${finances['loan_balance']:,.0f}"),
                    ui.p(f"Monthly Payment: ${finances['monthly_payment']:,.0f}"),
                    ui.p("Interest rate can be added in a future version."),
                ),
            ),
        ),
    )