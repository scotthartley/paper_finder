#! /usr/bin/env python3
"""
A simple python script that resolves journal article citations to online
repositories.

Requires three arguments:

1. The journal name/abbreviation.
2. The volume or year of the article, formatted as "v###" or "y###".
3. The first page of the article.

"""
import yaml, sys, webbrowser, os

# Path to YAML file containing journal definitions.
DEF_FILENAME = os.path.join(os.path.dirname(__file__), 'journal_def.yaml')

class ImproperInputError(Exception):
    pass

# Load journal definitions into the all_journals dictionary.
try:
    with open(DEF_FILENAME) as def_file:
        all_journals = yaml.load(def_file)
except yaml.parser.ParserError:
    print("Error loading database.")
    sys.exit(1)

try:
    # Will always be at least 4 arguments (scriptname, abbr., vol/year,
    # page).
    if len(sys.argv) < 4:
        raise ImproperInputError
    
    # Journal abbreviation. Note that there will not be spaces.
    target_j = "".join(sys.argv[1:-2]).lower()
    # Page number is last argument
    target_p = int(sys.argv[-1])

    # Loads the target volume or year.
    # Non-integer volumes are not supported at this time.
    target_v, target_y = None, None
    if sys.argv[-2][0] == 'v':
        target_v = int(sys.argv[-2][1:])
    elif sys.argv[-2][0] == 'y':
        target_y = int(sys.argv[-2][1:])
    elif sys.argv[-2][0].isdigit():
        target_v = int(sys.argv[-2])
    if target_v == None and target_y == None:
        raise ImproperInputError

# Catch incorrect input and exit.
except ValueError:
    print('Argument must be in format "j abbr {v/y}### ####".')
    sys.exit(1)
except ImproperInputError:
    print('Argument must be in format "j abbr {v/y}### ####".')
    sys.exit(1)

# Finds the correct journal in the library and assigns to journal
journal = None
for j in all_journals:
    if target_j in j['names']:
        journal = j
        break

if not journal:
    print('Journal not in YAML index.')
    sys.exit(1)


exact_journal = None
try:
    # If no "iterations" key, the actual journal used is just "journal".
    # Only if it falls after the start year/volume, though.
    if not 'iterations' in journal and (
            ('start_vol' in journal 
                and target_v 
                and target_v >= journal['start_vol']) or
            ('start_year' in journal 
                and target_y 
                and target_y >= journal['start_year'])):
        exact_journal = journal

    # If there is an "iterations" key, need to determine which one
    # applies to the target article.
    elif target_y:
        for j in journal['iterations']:
            if target_y >= j['start_year'] \
                    and (not 'end_year' in j \
                    or target_y <= j['end_year']):
                exact_journal = j
                break
    elif target_v:
        for j in journal['iterations']:
            # Necessary if some iterations don't have start_vol.
            if 'start_vol' in j:
                if target_v >= j['start_vol'] \
                        and (not 'end_vol' in j \
                        or target_v <= j['end_vol']):
                    exact_journal = j
                    break

except KeyError:
    print('Journal iteration not in YAML index.')
    sys.exit(0)

else:
    if not exact_journal:
        print('Journal for this timeframe not in YAML index.')
        sys.exit(0)

# Convert year <-> volume if makes sense for that journal, as indicated
# by existence of start keys. This only makes sense if there is one
# volume per year.
if not target_y and 'start_year' in exact_journal:
    target_y = (target_v - exact_journal['start_vol']) \
               + exact_journal['start_year']
if not target_v and 'start_vol' in exact_journal:
    target_v = (target_y - exact_journal['start_year']) \
               + exact_journal['start_vol']

# Determine the URL.
paper_url = exact_journal['url'].replace('{vol}', str(target_v))\
                          .replace('{year}', str(target_y))\
                          .replace('{page}', str(target_p))

# Open web browser.
# webbrowser.open(paper_url)
browser = webbrowser.get('safari') # Workaround for bug in macOS 10.12.5
browser.open(paper_url)
