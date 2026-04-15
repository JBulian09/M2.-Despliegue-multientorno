from pathlib import Path
import subprocess

repo_root = Path('/workspaces/M2.-Despliegue-multientorno')

index_html = """<!DOCTYPE html>
<html lang=\"es\">
<head>
<meta charset=\"UTF-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
<title>Release Board Básico</title>
<link rel=\"stylesheet\" href=\"style.css\" />
</head>
<body>
<main class=\"container\">
<section class=\"hero\">
<p class=\"eyebrow\">Laboratorio básico</p>
<h1>Release Board</h1>
<p class=\"subtitle\">
Práctica inicial de versiones y multientornos con HTML, CSS y JavaScript.
</p>
</section>
<section class=\"grid\">
<article class=\"card highlight\">
<h2>Entorno</h2>
<p id=\"environment\" class=\"badge\">cargando...</p>
</article>
<article class=\"card\">
<h2>Versión</h2>
<p id=\"version\" class=\"mono\">cargando...</p>
</article>
<article class=\"card\">
<h2>Última actualización</h2>
<p id=\"updatedAt\">cargando...</p>
</article>
</section>
<section class=\"card\">
<h2>Cambios de esta versión</h2>
<ul id=\"changes\"></ul>
</section>
</main>
<script src=\"config.js\"></script>
<script src=\"app.js\"></script>
</body>
</html>
"""

style_css = ":root {\nfont-family: Arial, Helvetica, sans-serif;\ncolor: #f8fafc;\nbackground:\nlinear-gradient(180deg, #1e3a5f 0%, #0f172a 60%, #020617 100%);\n}\n* {\nbox-sizing: border-box;\n}\nbody {\nmargin: 0;\nmin-height: 100vh;\n}\n.container {\nmax-width: 900px;\nmargin: 0 auto;\npadding: 40px 20px 60px;\n}\n.hero {\nmargin-bottom: 24px;\n}\n.eyebrow {\ntext-transform: uppercase;\nletter-spacing: 0.12em;\nfont-size: 0.8rem;\ncolor: #93c5fd;\n}\n.subtitle {\nmax-width: 700px;\ncolor: #cbd5e1;\n}\n.grid {\ndisplay: grid;\ngrid-template-columns: repeat(auto-fit, minmax(220px, 1fr));\ngap: 16px;\nmargin-bottom: 16px;\n}\n.card {\nbackground: rgba(15, 23, 42, 0.82);\nborder: 1px solid rgba(148, 163, 184, 0.2);\nborder-radius: 16px;\npadding: 18px;\n}\n.highlight {\nborder-color: rgba(59, 130, 246, 0.5);\n}\n.badge {\ndisplay: inline-block;\nbackground: #2563eb;\npadding: 6px 12px;\nborder-radius: 999px;\nfont-weight: bold;\ntext-transform: uppercase;\n}\n.mono {\nfont-family: Consolas, \"Courier New\", monospace;\ncolor: #fde68a;\n}\nul {\npadding-left: 20px;\n}\n"

app_js = """const config = window.APP_CONFIG;\ndocument.getElementById(\"environment\").textContent = config.environment;\ndocument.getElementById(\"version\").textContent = config.version;\ndocument.getElementById(\"updatedAt\").textContent = config.updatedAt;\nconst changesList = document.getElementById(\"changes\");\nconfig.changes.forEach((change) => {\n  const item = document.createElement(\"li\");\n  item.textContent = change;\n  changesList.appendChild(item);\n});\n"""

branch_configs = {
    'develop': {
        'environment': 'develop',
        'version': 'v0.1.0-dev',
        'updatedAt': '2026-04-09',
        'changes': [
            'Se creó la primera versión del laboratorio',
            'Se agregó una vista de entorno y versión',
            'Se preparó la estructura para trabajar con ramas'
        ]
    },
    'staging': {
        'environment': 'staging',
        'version': 'v0.1.0-staging',
        'updatedAt': '2026-04-10',
        'changes': [
            'Se agregó la rama staging para pruebas',
            'Se validó la página y configuración de entorno',
            'Preparación para publicar en GitHub Pages'
        ]
    },
    'main': {
        'environment': 'production',
        'version': 'v0.1.0',
        'updatedAt': '2026-04-10',
        'changes': [
            'Versión estable en main',
            'Configuración de GitHub Pages en staging',
            'Base para despliegue multientorno'
        ]
    }
}

for branch, cfg in branch_configs.items():
    print(f'\nChecking out {branch}...')
    subprocess.run(['git', '-C', str(repo_root), 'checkout', branch], capture_output=True, text=True)
    (repo_root / 'index.html').write_text(index_html)
    (repo_root / 'style.css').write_text(style_css)
    (repo_root / 'app.js').write_text(app_js)
    config_text = 'window.APP_CONFIG = {\n'
    config_text += f'  environment: "{cfg["environment"]}",\n'
    config_text += f'  version: "{cfg["version"]}",\n'
    config_text += f'  updatedAt: "{cfg["updatedAt"]}",\n'
    config_text += '  changes: [\n'
    for change in cfg['changes']:
        config_text += f'    "{change}",\n'
    config_text += '  ]\n};\n'
    (repo_root / 'config.js').write_text(config_text)
    result = subprocess.run(['git', '-C', str(repo_root), 'add', 'index.html', 'style.css', 'app.js', 'config.js'], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    status = subprocess.run(['git', '-C', str(repo_root), 'status', '--short'], capture_output=True, text=True).stdout
    if status.strip():
        result = subprocess.run(['git', '-C', str(repo_root), 'commit', '-m', f'Add root site files and config for {branch}'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    else:
        print('No changes to commit on', branch)
    result = subprocess.run(['git', '-C', str(repo_root), 'push', '-u', 'origin', branch], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

print('\nDone. Root files are committed and pushed on each branch.')
