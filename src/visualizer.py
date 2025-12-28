import io
from langchain_core.runnables.graph import MermaidDrawMethod
from orchestrator import build_workflow
from PIL import Image

app = build_workflow()
png_bytes = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

output_filename = "workflow_visualization.png"
with open(output_filename, "wb") as f:
    f.write(png_bytes)
    
print(f'Saved visualization as: {output_filename}')