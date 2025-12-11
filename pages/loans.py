from math import log, ceil
from shiny import ui
from shinywidgets import output_widget


def loans_ui(finances: dict):
    # Core values from finances
    loan_balance = float(finances.get("loan_balance", 0) or 0)
    monthly_payment = float(finances.get("monthly_payment", 0) or 0)

    # Optional interest rate (annual %, e.g., 6.5 for 6.5% APR)
    raw_interest = finances.get("interest_rate", None)
    apr = None
    has_valid_interest = False

    if raw_interest is not None:
        try:
            apr = float(raw_interest)
            if apr > 0:
                has_valid_interest = True
        except (TypeError, ValueError):
            has_valid_interest = False

    # ------ PAYOFF + AMORTIZATION CALCULATION ------

    months_to_payoff = None
    years_to_payoff = None
    schedule_rows = []  # for amortization snapshot table

    if has_valid_interest and monthly_payment > 0 and loan_balance > 0:
        r = apr / 100.0 / 12.0  # monthly interest rate

        # If payment is too small to cover interest, loan never pays off
        if monthly_payment > loan_balance * r:
            # Amortization formula: n = ln(PMT / (PMT - r*P)) / ln(1+r)
            try:
                n = log(monthly_payment / (monthly_payment - r * loan_balance)) / log(
                    1 + r
                )
                months_to_payoff = ceil(n)
                years_to_payoff = months_to_payoff / 12.0

                # Build a limited amortization schedule (up to 12 months, max 360)
                balance = loan_balance
                max_months = min(months_to_payoff, 360)
                for m in range(1, min(max_months, 12) + 1):
                    interest_paid = balance * r
                    principal_paid = monthly_payment - interest_paid
                    if principal_paid < 0:
                        principal_paid = 0
                    ending_balance = max(balance - principal_paid, 0)

                    schedule_rows.append(
                        {
                            "month": m,
                            "starting": balance,
                            "interest": interest_paid,
                            "principal": principal_paid,
                            "ending": ending_balance,
                        }
                    )

                    if ending_balance <= 0:
                        break
                    balance = ending_balance

            except (ValueError, ZeroDivisionError):
                months_to_payoff = None
                years_to_payoff = None

    # Fallback: simple payoff estimate without interest if we couldn't do the math above
    if months_to_payoff is None and monthly_payment > 0 and loan_balance > 0:
        months_to_payoff = loan_balance / monthly_payment
        years_to_payoff = months_to_payoff / 12.0

    # Text helpers
    if has_valid_interest and apr is not None:
        interest_text = f"{apr:.2f}% APR"
    else:
        interest_text = (
            "Not set yet. Add an interest rate in your financial details "
            "to see a more accurate payoff timeline."
        )

    payoff_text = (
        f"If you keep paying about ${monthly_payment:,.0f} per month, you could "
        f"pay off ${loan_balance:,.0f} in roughly {months_to_payoff:,.0f} months "
        f"(about {years_to_payoff:,.1f} years)."
        if months_to_payoff and months_to_payoff > 0
        else "Add a monthly payment amount to see an estimated payoff timeline."
    )

    interest_note_text = (
        "This estimate includes the effect of interest, so a higher APR means "
        "it will take longer and cost more overall."
        if has_valid_interest and apr is not None
        else "Right now this estimate is approximate. Once you add an interest "
        "rate, it will better reflect how interest affects your payoff."
    )

    # ------ UI ------

    # Amortization table UI (only if we built rows)
    if schedule_rows:
        table_body = []
        for row in schedule_rows:
            table_body.append(
                ui.tags.tr(
                    ui.tags.td(str(row["month"])),
                    ui.tags.td(f"${row['starting']:,.0f}"),
                    ui.tags.td(f"${row['interest']:,.0f}"),
                    ui.tags.td(f"${row['principal']:,.0f}"),
                    ui.tags.td(f"${row['ending']:,.0f}"),
                )
            )

        amortization_table = ui.tags.table(
            {"class": "table table-sm"},
            ui.tags.thead(
                ui.tags.tr(
                    ui.tags.th("Month"),
                    ui.tags.th("Starting Balance"),
                    ui.tags.th("Interest"),
                    ui.tags.th("Principal"),
                    ui.tags.th("Ending Balance"),
                )
            ),
            ui.tags.tbody(*table_body),
        )
    else:
        amortization_table = ui.p(
            "Once you add both a monthly payment and a valid interest rate, "
            "you’ll see a snapshot of your first few months of payments here."
        )

    return ui.page_fluid(
        ui.h2("Loan Overview", class_="text-center mb-3"),

        # ----- TOP ROW: CHART + CORE DETAILS (chart unchanged) -----
        ui.row(
            ui.column(
                7,
                ui.card(
                    ui.card_header("Loan Balance Trend"),
                    # Plotly chart (UNCHANGED – still uses loan_line)
                    output_widget("loan_line"),
                ),
            ),
            ui.column(
                5,
                ui.card(
                    ui.card_header("Loan Details"),
                    ui.p(f"Current Balance: ${loan_balance:,.0f}"),
                    ui.p(f"Monthly Payment: ${monthly_payment:,.0f}"),
                    ui.p(f"Interest Rate: {interest_text}"),
                    ui.hr(),
                    ui.p(payoff_text),
                    ui.p(interest_note_text, class_="text-muted"),
                ),
            ),
        ),

        ui.br(),

        # ----- SECOND ROW: AMORTIZATION SNAPSHOT TABLE -----
        ui.row(
            ui.column(
                12,
                ui.card(
                    ui.card_header("Amortization Snapshot"),
                    ui.p(
                        "Here’s a peek at how your first few payments are split "
                        "between interest and principal."
                    ),
                    amortization_table,
                ),
            )
        ),
    )
