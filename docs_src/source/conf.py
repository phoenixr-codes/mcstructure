#:==========================================
# Sphinx Documentation Builder Configuration
#:==========================================


#########
# Imports

from datetime import date
from pathlib import Path
import sys


#############
# Change Path

sys.path.insert(0, str(Path('.').parent.parent))
sys.path.append(str(Path('./_ext').resolve()))


#####################
# Project Information

project = 'mcstructure'
copyright = f'{date.today().year}, phoenixR'
author = 'phoenixR'
release = '0.0.1b3'


###############
# Configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]


#######################
# Autodoc Configuration

autodoc_default_options = dict.fromkeys('''
    members
    inherited-members
    undoc-members
    '''.split(),
    True
)
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autoclass_content = 'both'


############
# Find Files

templates_path = ['_templates']
exclude_patterns = []


###########################
# HTML Output Configuration

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['css/style.css']
html_theme_options = {
    "single_page": True,
    "use_download_button": True,
    "repository_url": "https://github.com/phoenixr-codes/mcstructure/",
    "use_repository_button": True,
}
