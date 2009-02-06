TEX_COMPILER=pdflatex

$PHONY: all

all: clean build

clean:
	@rm -f *.pdf
	@rm -f *.log
	@rm -f *.aux
	@rm -f *.toc

movefiles:
	@mkdir -p PDF
	@mkdir -p Log
	@mv *.pdf PDF/
	@mv *.log Log/
	@mv *.aux Log/
	@mv *.toc Log/

build: Architecture_Notebook.pdf Develop_Technical_Vision.pdf Glossary.pdf Projektplan.pdf RiskList.pdf System-WideRequirements.pdf Use-case Model.pdf Use-case.pdf Vision.pdf movefiles

Architecture_Notebook.pdf:
	${TEX_COMPILER} "Architecture Notebook.tex"

Develop_Technical_Vision.pdf:
	${TEX_COMPILER} "Develop Technical Vision.tex"

Glossary.pdf:
	${TEX_COMPILER} Glossary.tex

Projektplan.pdf:
	${TEX_COMPILER} Projektplan.tex

RiskList.pdf:
	${TEX_COMPILER} RiskList.tex

System-WideRequirements.pdf:
	${TEX_COMPILER} System-WideRequirements.tex

Use-case Model.pdf:
	${TEX_COMPILER} Use-case Model.tex

Use-case.pdf:
	${TEX_COMPILER} Use-case.tex

Vision.pdf:
	${TEX_COMPILER} Vision.tex

