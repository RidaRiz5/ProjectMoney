from shiny import ui

def chatbot_ui():
    return ui.page_fluid(
        ui.card(
            ui.card_header("FYWISE Chatbot"),
            ui.input_text_area("chat_input", "Ask something about your money:"),
            ui.input_action_button("send_chat", "Send", class_="btn-primary mt-2"),
            ui.br(),
            ui.output_text("chat_reply"),
        )
    )