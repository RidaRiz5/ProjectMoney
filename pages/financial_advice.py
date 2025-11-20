from shiny import ui

def financial_advice_ui():
    return ui.page_fluid(

        ui.h2("Financial Advice", class_="text-center mb-4"),

        # ---------- 50/30/20 RULE ----------
        ui.card(
            ui.card_header("The 50/30/20 Rule"),

            ui.p("The 50/30/20 rule is a basic budgeting rule that breaks your finances into 3 categories:"),

            ui.tags.ul(
                ui.tags.li(ui.tags.b("50% Needs: "), "Housing, groceries, utilities, transport"),
                ui.tags.li(ui.tags.b("30% Wants: "), "Entertainment, eating out, subscriptions"),
                ui.tags.li(ui.tags.b("20% Savings/Debt: "), "Emergency fund, retirement, loans"),
            ),

            ui.p("Needs include: rent, utilities, groceries, insurance, and transportation."),
            ui.p("Wants include: entertainment, eating out, shopping, subscriptions."),
            ui.p("Savings/debt includes: emergency savings, retirement accounts, and loan payments."),

            ui.div("💡 Tip: Use this rule as a guide, then adjust based on your lifestyle!",
                   class_="tip-box")
        ),

        ui.br(),

        # ---------- SMART GOALS ----------
        ui.card(
            ui.card_header("Creating SMART Financial Goals"),

            ui.p("SMART goals help you create realistic plans you can actually follow:"),

            ui.tags.ul(
                ui.tags.li(ui.tags.b("S: "), "Specific"),
                ui.tags.li(ui.tags.b("M: "), "Measurable"),
                ui.tags.li(ui.tags.b("A: "), "Achievable"),
                ui.tags.li(ui.tags.b("R: "), "Relevant"),
                ui.tags.li(ui.tags.b("T: "), "Time-bound"),
            ),

            ui.div("💡 Tip: Break big goals into smaller steps.",
                   class_="tip-box")
        ),

        ui.br(),

        # ---------- RETIREMENT ----------
        ui.card(
            ui.card_header("Retirement Savings"),

            ui.tags.ul(
                ui.tags.li(ui.tags.b("401(k) / 403(b): "), "Employer-sponsored plans, often with matching."),
                ui.tags.li(ui.tags.b("Traditional IRA: "), "Tax-deductible contributions, tax-deferred growth."),
                ui.tags.li(ui.tags.b("Roth IRA: "), "Tax-free withdrawals in retirement."),
                ui.tags.li(ui.tags.b("HSA: "), "Triple tax advantage for medical savings."),
                ui.tags.li(ui.tags.b("Brokerage Account: "), "Flexible investing with no contribution limits."),
            ),

            ui.div("💡 Tip: Always take your employer’s full match. Ot's free money.",
                   class_="tip-box")
        ),

        ui.br(),

        # ---------- PRINCIPLES ----------
        ui.card(
            ui.card_header("Core Financial Principles"),

            ui.tags.ul(
                ui.tags.li(ui.tags.b("Pay Yourself First: "), "Save before spending."),
                ui.tags.li(ui.tags.b("Live Below Your Means: "), "Spend less than you earn."),
                ui.tags.li(ui.tags.b("Track Your Spending: "), "Awareness creates control."),
                ui.tags.li(ui.tags.b("Emergency Fund: "), "3–6 months of expenses saved."),
                ui.tags.li(ui.tags.b("Avoid High-Interest Debt: "), "Pay off credit cards quickly."),
                ui.tags.li(ui.tags.b("Compound Interest: "), "Start investing early."),
                ui.tags.li(ui.tags.b("Diversify Investments: "), "Spread out risk."),
                ui.tags.li(ui.tags.b("Increase Savings Over Time: "), "Raise contributions as income grows."),
                ui.tags.li(ui.tags.b("Review Goals Yearly: "), "Adjust as life changes."),
            ),

            ui.div("💡 Tip: Focus on long-term habits, not perfection.",
                   class_="tip-box")
        ),
    )