.PHONY: qa qa-full proofread-mark proofread-check qa-references-style qa-citation-web qa-citation-web-core qa-citations

PAPER_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

proofread-mark:
	@python "$(PAPER_DIR)scripts/qa_proofread_gate.py" --mark

proofread-check:
	@python "$(PAPER_DIR)scripts/qa_proofread_gate.py" --check

qa-references-style:
	@python "$(PAPER_DIR)scripts/qa_references_style.py" \
		--fix \
		--report "$(PAPER_DIR)reports/qa_references_style.md"

qa-citation-web:
	@python "$(PAPER_DIR)scripts/qa_citation_web.py" \
		--scope all \
		--report "$(PAPER_DIR)reports/qa_citation_web.md"

qa-citation-web-core:
	@python "$(PAPER_DIR)scripts/qa_citation_web.py" \
		--scope core \
		--report "$(PAPER_DIR)reports/qa_citation_web_prewrite.md"

qa-citations:
	@python "$(PAPER_DIR)scripts/qa_citations.py" \
		--sections-dir "$(PAPER_DIR)sections" \
		--bib "$(PAPER_DIR)refs/references.bib" \
		--report "$(PAPER_DIR)reports/qa_citations.md"

qa: qa-references-style qa-citation-web qa-citations
	@mkdir -p "$(PAPER_DIR)exports"
	@cd "$(PAPER_DIR)" && pandoc --defaults=pandoc.yaml

qa-full: proofread-check qa
