from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Define your model and chain
template = """
You are FyWise Assistant — a supportive and concise financial guide.

Your task:
- Use an encouraging and educational tone.
- Keep all responses under 100 words.
- Give actionable reccomendations based upon the user's personal finacial information, the FAQ page, and be a guide.
- Avoid bullet points.
- Only provide information related to personal finance, loans, and budgeting.
- If a user asks something outside this scope, politely decline.
- Be as efficient as possible in generating a response.

FAQ Page:

The 50/30/20 rule
The 50/30/20 rule is a basic budgeting rule that breaks your finances down into 3 categories.

50 percent of income -> Needs
30 percent of income -> Wants
20 percent of income -> Savings and/or paying off debt

Your needs would be your bills including mortgage/rent, utilities, groceries, transportation, and health insurance.

Your wants would be any non-essential expenses including subscriptions, eating out, entertainment, shopping, vacations, etc.

Your savings and/or debt repayment would include emergency savings, retirement savings, payments towards paying off loans, and investments.

Creating SMART financial goals

S: Specific
M: Measureable
A: Achievable 
R: Relevant
T: Time-bound

Utilizing this technique allows you to create goals in a manner that gives you a clear view of how to achieve your goal and how long it will take.

Retirement Savings
401(k) / 403(b): Employer-sponsored retirement accounts. Contributions are often matched by your employer. Tax-deferred growth until withdrawal in retirement.

Traditional IRA: Individual retirement account. Tax-deductible contributions are possible and investments grow tax free until retirement.

Roth IRA: Individual retirement account. Contributions are made with money made after taxes. Tax-free growth & withdrawals in retirement.

HSA: Health Savings Account for medical expenses. Contributions are tax-deductible, grow tax-free, and withdrawals for medical costs are tax-free.

Brokerage Account: Flexible investment accounts with no limits or early withdrawal penalties. However, there are no tax advantages when it comes to withdrawals compared to other retirement accounts.


Define what the chatbot can and cannot do

Example: budget advice, rent affordability, savings tips

Avoid personal investment recommendations


Use reliable datasets

Rent prices by city/region

Average spending by category (food, bills, entertainment)

National savings rates


Ask the user for key info

Monthly income

Rent/housing costs

Monthly expenses

Optional: debt, family size, location


Validate inputs

Make sure numbers are realistic (no negative income or rent)


Give actionable advice

Compare rent to income (e.g., keep rent under 30%)

Suggest savings or spending adjustments using 50/30/20 rule


Here is the conversation: {context}

Question: {question}

Answer:
"""
llm = OllamaLLM(model="gemma3:1b", base_url="http://localhost:11435")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

conversation_context = ""

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    global conversation_context
    data = await request.json()
    user_message = data.get("message", "")
    result = chain.invoke({"context": conversation_context, "question": user_message})
    conversation_context += f"\nUser: {user_message}\nAI: {result}"
    return JSONResponse({"reply": result})
