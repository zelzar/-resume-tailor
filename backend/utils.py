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
    
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", f"{output_name}.tex"],
        cwd=output_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", f"{output_name}.tex"],
        cwd=output_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    return pdf_file
