import os
import subprocess
import re

def sanitize_latex(text: str) -> str:
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'[#$%&_{}\\^~]', '', text)
    text = text.replace('|', '')
    return text.strip()

def render_latex_template(template_path: str, context: dict, output_dir: str, output_name: str):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    fitkind_bullets = context.get('fitkind_bullets', [])
    cmindset_bullets = context.get('cmindset_bullets', [])
    
    all_bullets = fitkind_bullets + cmindset_bullets
    
    for bullet in all_bullets:
        placeholder = '{{ bullet }}'
        if placeholder in template_content:
            template_content = template_content.replace(placeholder, bullet, 1)
    
    for key, value in context.items():
        if isinstance(value, str) and key not in ['fitkind_bullets', 'cmindset_bullets']:
            template_content = template_content.replace('{{ ' + key + ' }}', value)
            template_content = template_content.replace('{{' + key + '}}', value)
    
    tex_file = os.path.join(output_dir, f"{output_name}.tex")
    pdf_file = os.path.join(output_dir, f"{output_name}.pdf")
    
    with open(tex_file, "w") as f:
        f.write(template_content)
    
    # Run pdflatex twice to resolve references. Capture output to aid debugging when it fails.
    for i in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"{output_name}.tex"],
            cwd=output_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            # Include the pdflatex stdout/stderr in the raised exception so FastAPI logs it.
            raise RuntimeError(
                f"pdflatex failed (run {i+1}/2) with return code {result.returncode}\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
    
    return pdf_file
