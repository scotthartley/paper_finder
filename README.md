# paper_finder: A Python script that resolves citations to scientific journal articles

paper_finder is a Python 3 script that accepts a journal citation as its input and attempts to open
the default web browser to the online article. Journal information is stored in a YAML database.
I'm an organic chemist, so the default database is populated with chemistry journals. Contribution
of additional journals to `journal_def.yaml` is welcome.

It is intended as a command-line utility, so input should be in the format `paper_finder.py abb
v123 1234`, where abb is the abbreviation/name of the journal, 123 is the volume number and 1234 is
the page number. When possible, it can be used to find papers by year with `paper_finder.py abb
y1999 1234`. If the v/y prefix is omitted, it is assumed that the number is a volume number. It is
very handy when coupled with a launcher, like [Alfred][].

The script is inspired by the [Chemistry Reference Resolver][]. Frankly, the Chemistry Reference
Resolver is a more powerful tool, but this utility is easily customized to add/remove journals and
change abbreviations, which can be handy.

[Alfred]: https://www.alfredapp.com
[Chemistry Reference Resolver]: http://chemsearch.kovsky.net
