#:==========================================
# Sphinx Documentation Builder Configuration
#:==========================================


#####################
# Project Information

project = 'mcstructure'
copyright = '2023, Jonas da Silva'
author = 'Jonas da Silva'
release = '0.0.1b4'


###############
# Configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',

    'myst_parser',
    'sphinx_copybutton',
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
autodoc_typehints = 'both'
autoclass_content = 'both'


############
# Find Files

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


###########################
# HTML Output Configuration

html_theme = 'furo'
html_logo = "../logo.png"
html_favicon = "../logo.png"
html_static_path = ['_static']

