#
# CSrankings
# http://csrankings.org
# Copyright (C) 2017 by Emery Berger <http://emeryberger.org>
# See COPYING for license information.
#

TARGETS = csrankings.js generated-author-info.csv

.PHONY: home-pages scholar-links fix-affiliations update-dblp clean-dblp download-dblp shrink-dblp

PYTHON = python2.7
PYPY   = pypy

all: generated-author-info.csv csrankings.js # fix-affiliations home-pages scholar-links

clean:
	rm $(TARGETS)

csrankings.js: csrankings.ts
	@echo "Rebuilding JavaScript code."
	tsc --project tsconfig.json
	closure-compiler --js csrankings.js > csrankings.min.js

update-dblp:
	$(MAKE) download-dblp
	$(MAKE) clean-dblp
	@echo "Done."

clean-dblp:
	@echo "Fixing character encodings."
	sh ./util/fix-dblp.sh
	mv dblp-fixed.xml dblp.xml
	$(MAKE) shrink-dblp

download-dblp:
	@echo "Downloading from DBLP."
	rm -f dblp.xml.gz
	wget http://dblp.org/xml/dblp.xml.gz

shrink-dblp:
	@echo "Shrinking the DBLP file."
	basex -c filter.xq > dblp2.xml
	gzip dblp2.xml
	mv dblp.xml.gz dblp-original.xml.gz
	mv dblp2.xml.gz dblp.xml.gz

faculty-affiliations.csv homepages.csv scholar.csv: csrankings.csv
	@echo "Splitting main datafile (csrankings.csv)."
	@$(PYTHON) util/split-csv.py
	@echo "Done."

clean-csrankings:
	@echo "Cleaning."
	@$(PYTHON) util/clean-csrankings.py
	@echo "Done."

home-pages: faculty-affiliations.csv homepages.csv
	@echo "Rebuilding home pages (homepages.csv)."
	@$(PYTHON) util/make-web-pages.py
	@echo "Cleaning home pages."
	@$(PYTHON) util/clean-web-pages.py
	@mv homepages-sorted.csv homepages.csv
	@echo "Done."

scholar-links: faculty-affiliations.csv homepages.csv
	@echo "Rebuilding Google Scholar links (scholar.csv)."
	@$(PYTHON) util/make-scholar-links.py
	@echo "Cleaning Scholar links."
	@$(PYTHON) util/clean-scholar-links.py
	@echo "Done."

fix-affiliations: faculty-affiliations.csv
	@echo "Updating affiliations."
	@$(PYTHON) util/fix-affiliations.py | sort -k2 -t"," | uniq > /tmp/f1.csv
	@echo "name,affiliation" | cat - /tmp/f1.csv >  /tmp/f2.csv
	@rm /tmp/f1.csv
	@mv /tmp/f2.csv faculty-affiliations.csv

faculty-coauthors.csv: dblp.xml.gz util/generate-faculty-coauthors.py util/csrankings.py
	@echo "Rebuilding the co-author database (faculty-coauthors.csv)."
	$(PYTHON) util/generate-faculty-coauthors.py
	@echo "Done."

generated-author-info.csv: faculty-affiliations.csv dblp.xml.gz util/regenerate_data.py util/csrankings.py
	@echo "Rebuilding the publication database (generated-author-info.csv)."
	@$(PYPY) util/regenerate_data.py
	@echo "Done."

collab-graph: generated-author-info.csv faculty-coauthors.csv
	@echo "Generating the list of all publications (all-author-info.csv)."
	$(PYTHON) util/generate-all-pubs.py
	@echo "Building collaboration graph data."
	$(PYTHON) util/make-collaboration-graph.py
