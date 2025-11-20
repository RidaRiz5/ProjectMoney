from shiny import ui

def login_ui():
    return ui.page_fluid(
        ui.div(
            ui.card(
                ui.card_header("Welcome to FYWISE"),
                ui.p("Log in or create an account to explore your financial dashboard."),
                ui.input_text("username", "Username"),
                ui.input_password("password", "Password"),
                ui.div(
                    ui.input_action_button("login_btn", "Login", class_="btn-primary me-2"),
                    ui.input_action_button("signup_btn", "Sign Up", class_="btn-success"),
                    class_="mt-2 text-center",
                ),
                ui.p(
                    "Tip: Use a simple demo username like 'testuser' for now.",
                    class_="mt-3 text-muted",
                ),
            ),
            class_="login-container"
        )
    )