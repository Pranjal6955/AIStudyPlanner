import os
import sys
from typing import TypedDict
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.spinner import Spinner
from rich.live import Live
from rich.markdown import Markdown
from rich import box

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END

# ─────────────────────────────────────────
# Setup
# ─────────────────────────────────────────
load_dotenv()
console = Console()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    console.print(Panel(
        "[bold red]GROQ_API_KEY is not set.[/bold red]\n\n"
        "Add it to your [cyan].env[/cyan] file:\n"
        "  [green]GROQ_API_KEY=gsk_...[/green]\n\n"
        "Get a free key at: [link=https://console.groq.com/keys]console.groq.com/keys[/link]",
        title="[red]⛔  Missing API Key[/red]",
        border_style="red",
    ))
    sys.exit(1)

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=float(os.getenv("GROQ_TEMPERATURE", "0.7")),
    groq_api_key=GROQ_API_KEY,
)


# ─────────────────────────────────────────
# Shared State
# ─────────────────────────────────────────
class AgentState(TypedDict):
    user_input: str
    analyzed_goal: str
    plan: str
    resources: str
    final_output: str


# ─────────────────────────────────────────
# Helper: run an agent step with a spinner
# ─────────────────────────────────────────
def run_step(label: str, emoji: str, fn, state: AgentState) -> dict:
    spinner_text = Text()
    spinner_text.append(f"  {emoji}  {label} ", style="bold cyan")
    spinner_text.append("running...", style="dim")

    with Live(Spinner("dots", text=spinner_text), console=console, refresh_per_second=12):
        result = fn(state)

    console.print(f"  [bold green]✔[/bold green]  [cyan]{label}[/cyan] [dim]done[/dim]")
    return result


# ─────────────────────────────────────────
# Agent 1: Goal Analyzer
# ─────────────────────────────────────────
def goal_analyzer(state: AgentState):
    prompt = f"""
    Analyze the user's goal and extract:
    - Main objective
    - Duration
    - Skill level (beginner/intermediate/advanced)

    User Input: {state['user_input']}
    """
    response = llm([HumanMessage(content=prompt)])
    return {"analyzed_goal": response.content}


# ─────────────────────────────────────────
# Agent 2: Planner Agent
# ─────────────────────────────────────────
def planner_agent(state: AgentState):
    prompt = f"""
    Create a structured study plan based on:

    {state['analyzed_goal']}

    Include:
    - Weekly breakdown
    - Daily tasks
    """
    response = llm([HumanMessage(content=prompt)])
    return {"plan": response.content}


# ─────────────────────────────────────────
# Agent 3: Resource Agent
# ─────────────────────────────────────────
def resource_agent(state: AgentState):
    prompt = f"""
    Suggest best learning resources for this plan:

    {state['plan']}

    Include:
    - YouTube
    - Docs
    - Courses
    """
    response = llm([HumanMessage(content=prompt)])
    return {"resources": response.content}


# ─────────────────────────────────────────
# Agent 4: Reviewer Agent
# ─────────────────────────────────────────
def reviewer_agent(state: AgentState):
    prompt = f"""
    Review and improve the final study plan:

    PLAN:
    {state['plan']}

    RESOURCES:
    {state['resources']}

    Make it:
    - Clear
    - Actionable
    - Motivating
    """
    response = llm([HumanMessage(content=prompt)])
    return {"final_output": response.content}


# ─────────────────────────────────────────
# Build LangGraph Workflow (with CLI hooks)
# ─────────────────────────────────────────
def run_pipeline(user_input: str) -> str:
    state: AgentState = {
        "user_input": user_input,
        "analyzed_goal": "",
        "plan": "",
        "resources": "",
        "final_output": "",
    }

    console.print()
    console.print(Rule("[bold]Running agents[/bold]", style="bright_black"))
    console.print()

    # Step 1
    state.update(run_step("Goal Analyzer", "🔍", goal_analyzer, state))
    # Step 2
    state.update(run_step("Planner", "📅", planner_agent, state))
    # Step 3
    state.update(run_step("Resource Finder", "📚", resource_agent, state))
    # Step 4
    state.update(run_step("Reviewer", "✨", reviewer_agent, state))

    return state["final_output"]


# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
def main():
    # Banner
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🎓  AI Study Planner[/bold cyan]\n"
        "[dim]Powered by Groq · LangChain · LangGraph[/dim]",
        border_style="cyan",
        box=box.DOUBLE,
    ))
    console.print()

    # Input
    console.print("[bold white]What do you want to learn?[/bold white]")
    user_input = console.input("[bold cyan]❯ [/bold cyan]").strip()

    if not user_input:
        console.print("[red]No input provided. Exiting.[/red]")
        sys.exit(0)

    # Run pipeline
    final_output = run_pipeline(user_input)

    # Output
    console.print()
    console.print(Rule("[bold green]Your Study Plan[/bold green]", style="green"))
    console.print()
    console.print(Markdown(final_output))
    console.print()
    console.print(Rule(style="bright_black"))
    console.print("[dim]Tip: Copy the plan above or pipe output to a file:  python multi_agent_system.py > plan.md[/dim]")
    console.print()


if __name__ == "__main__":
    main()