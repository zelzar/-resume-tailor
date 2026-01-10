import os
import subprocess
import re
from jinja2 import Environment, FileSystemLoader

# --- sanitize Gemini output for LaTeX ---
def sanitize_latex(text: str) -> str:
    """
    Keep only safe characters: letters, numbers, space, comma, slash, dot
    Remove LaTeX special chars that break compilation.
    """
    return re.sub(r"[^A-Za-z0-9 ,/.\-]", "", text).strip()

# --- render Jinja LaTeX template and compile PDF ---
def render_latex(template_path: str, context: dict, output_dir: str, output_name: str):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    rendered_tex = template.render(**context)

    tex_file = os.path.join(output_dir, f"{output_name}.tex")
    pdf_file = os.path.join(output_dir, f"{output_name}.pdf")

    os.makedirs(output_dir, exist_ok=True)
    with open(tex_file, "w") as f:
        f.write(rendered_tex)

    # compile LaTeX PDF
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", tex_file],
        cwd=output_dir,
        stdout=subprocess.DEVNULL
    )
    return pdf_file
