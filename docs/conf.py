project = "Fabulous Collections"
author = "Ozek"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode", "sphinx.ext.githubpages"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "shibuya"
html_static_path = ["_static"]
html_theme_options = {
    "accent_color": "orange",
}
