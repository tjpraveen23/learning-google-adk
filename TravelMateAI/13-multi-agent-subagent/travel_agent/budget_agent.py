from google.adk.agents import Agent
from google.adk.models import LiteLlm
from .config import MODEL_NAME

budget_agent = Agent(
    name="BudgetAgent",
    model=LiteLlm(model=MODEL_NAME),
    instruction="""You are a travel budget expert.
                    Estimate travel expenses.
                    If the request is unrelated,
                    say: 'I only estimate travel budgets.' """
)