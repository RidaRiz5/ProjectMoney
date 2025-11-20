from shiny import ui

def create_account_ui():
    return ui.page_fluid(
        ui.h2("Create Your FYWISE Account", class_="text-center mb-4"),

        ui.row(
            ui.column(3),
            ui.column(
                6,
                ui.card(
                    ui.card_header("Start Your Journey"),

                    ui.input_text("first_name", "First Name:"),
                    ui.input_text("last_name", "Last Name:"),
                    ui.input_text("dob", "Date of Birth (YYYY-MM-DD):"),
                    ui.input_text("email", "Email:"),

                    ui.hr(),

                    ui.input_text("username_new", "Choose a Username:"),
                    ui.input_password("password_new", "Choose a Password:"),
                    ui.input_password("confirm_password_new", "Confirm Password:"),

                    ui.br(),

                    ui.div(
                        ui.input_action_button(
                            "create_account_btn",
                            "Create Account",
                            class_="btn-success w-100"
                        ),
                        class_="text-center"
                    ),
                ),
            ),
            ui.column(3),
        ),

        ui.br(),

        ui.div(
            ui.p("Already have an account?"),
            ui.input_action_button("go_login", "Back to Login", class_="btn-secondary"),
            class_="text-center"
        )
    )