from shiny import ui

def chatbot_ui():
    return ui.page_fluid(
        ui.div(
            {"class": "chat-page"},
            ui.div(
                {"class": "chat-container"},

                # ---- HEADER (fixed, no ui.header) ----
                ui.div(
                    {"class": "chat-header"},
                    ui.div(
                        {"class": "header-text"},
                        ui.h1("FyWise Assistant"),
                        ui.p(
                            "Empowering you to take control of your financial future.",
                            class_="tagline"
                        ),
                    ),
                ),

                # ---- CHAT BOX ----
                ui.div(
                    {"class": "chat-box", "id": "chat-box"},
                    ui.output_ui("chat_history"),
                ),

                # ---- INPUT FIELD ----
                ui.div(
                    {"class": "input-container"},
                    ui.input_text(
                        "chat_input",
                        label=None,
                        placeholder="Type your message...",
                        width="100%",
                    ),
                    ui.input_action_button(
                        "send_chat",
                        "Send",
                        class_="chat-send-btn",
                    ),
                ),
            ),
        )
    )
