# Build both companion papers and their six deliverables each.
#
#   make            both papers, all deliverables, then the QA gates
#   make accounts   paper A only
#   make ownership  paper B only
#   make qa         gates only, against whatever is currently built
#   make clean      remove build artifacts and deliverables
#
# Shared assets (figures, tables, results_macros.tex) live in ../paper and are
# referenced by relative path, so there is one source of truth for every
# measured value. references.bib is copied in because bibtex does not resolve a
# relative database path reliably here.

SHARED := ../paper
A      := accounts
B      := ownership
A_NAME := Labor_Backing_Accounts
B_NAME := Ownership_Not_Profit_Shifting

.PHONY: all accounts ownership qa clean figures macros

all: accounts ownership qa

figures:
	cd .. && python paper/gen_figures.py

macros:
	cd .. && python paper/gen_results_macros.py

accounts:
	$(MAKE) paper DIR=$(A) NAME=$(A_NAME)

ownership:
	$(MAKE) paper DIR=$(B) NAME=$(B_NAME)

# One paper: author PDF, anonymous PDF, title page PDF, and the three DOCX.
paper:
	cp $(SHARED)/references.bib $(DIR)/references.bib
	cd $(DIR) && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
	cd $(DIR) && bibtex main >/dev/null
	cd $(DIR) && pdflatex -interaction=nonstopmode main.tex >/dev/null
	cd $(DIR) && pdflatex -interaction=nonstopmode main.tex >/dev/null
	cd $(DIR) && pdflatex -jobname=main_anon -interaction=nonstopmode '\def\ANON{}\input{main.tex}' >/dev/null
	cd $(DIR) && bibtex main_anon >/dev/null
	cd $(DIR) && pdflatex -jobname=main_anon -interaction=nonstopmode '\def\ANON{}\input{main.tex}' >/dev/null
	cd $(DIR) && pdflatex -jobname=main_anon -interaction=nonstopmode '\def\ANON{}\input{main.tex}' >/dev/null
	cd $(DIR) && pdflatex -interaction=nonstopmode titlepage.tex >/dev/null
	cd $(DIR) && pdflatex -interaction=nonstopmode titlepage.tex >/dev/null
	cd $(DIR) && python ../_to_docx.py full >/dev/null
	cd $(DIR) && pandoc main_docx.tex -o "$(NAME).docx" --resource-path=$(SHARED)/figures
	cd $(DIR) && python ../_to_docx.py anon >/dev/null
	cd $(DIR) && pandoc main_docx.tex -o "$(NAME)_anon.docx" --resource-path=$(SHARED)/figures
	cd $(DIR) && pandoc titlepage.tex -o "$(NAME)_TitlePage.docx"
	@echo "built $(DIR): 6 deliverables"

qa:
	@echo "=== $(A) ==="
	cd $(A) && python ../_qa.py && python ../_anoncheck.py && python ../_count.py
	@echo
	@echo "=== $(B) ==="
	cd $(B) && python ../_qa.py && python ../_anoncheck.py && python ../_count.py

clean:
	rm -f $(A)/*.aux $(A)/*.bbl $(A)/*.blg $(A)/*.log $(A)/*.out $(A)/*.pdf \
	      $(A)/*.fls $(A)/*.fdb_latexmk $(A)/*.docx $(A)/main_docx.tex $(A)/references.bib
	rm -f $(B)/*.aux $(B)/*.bbl $(B)/*.blg $(B)/*.log $(B)/*.out $(B)/*.pdf \
	      $(B)/*.fls $(B)/*.fdb_latexmk $(B)/*.docx $(B)/main_docx.tex $(B)/references.bib
