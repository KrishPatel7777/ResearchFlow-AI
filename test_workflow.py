from graph.workflow import run_workflow

result = run_workflow({
    "task":"research",
    "topic":"Artificial Intelligence"
})
print(result["answer"])