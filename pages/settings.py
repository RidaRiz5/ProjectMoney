from shiny import ui

def settings_ui(username: str, finances: dict):

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

    return ui.page_fluid(
        ui.h2("Settings & Profile", class_="text-center mb-3"),

        ui.row(
            ui.column(
                6,
                ui.card(
                    ui.card_header("Profile Summary"),
                    ui.p(f"User: {username}"),
                    ui.p(f"Total Monthly Income: ${monthly_income:,.0f}"),
                    ui.p(f"Total Monthly Expenses: ${total_expenses:,.0f}"),
                ),
            ),
            ui.column(
                6,
                ui.card(
                    ui.card_header("Settings"),
                    ui.p("Manage your FYWISE experience:"),
                    ui.br(),
                    ui.input_action_button(
                        "go_finance_input",
                        "Edit Financial Details",
                        class_="btn btn-settings w-100 mb-2",
                    ),
                    ui.input_action_button(
                        "settings_notifications",
                        "Notification Preferences",
                        class_="btn btn-settings w-100 mb-2",
                    ),
                    ui.input_action_button(
                        "settings_goals",
                        "View / Edit Goals",
                        class_="btn btn-settings w-100 mb-2",
                    ),
                    ui.input_action_button(
                        "settings_export",
                        "Export My Data",
                        class_="btn btn-settings w-100",
                    ),
                    ui.p("Only 'Edit Financial Details' changes pages right now.", class_="mt-2 text-muted"),
                ),
            ),
        ),
    )