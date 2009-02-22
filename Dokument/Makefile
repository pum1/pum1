TEX_COMPILER=pdflatex
OUTPUT_DIR=PDF
LOG_DIR=Log

$PHONY: all

all: clean build

clean:
	@rm -rf ${OUTPUT_DIR}
	@rm -rf ${LOG_DIR}

build: \
	dirs \
	${OUTPUT_DIR}/Architecture_Notebook.pdf \
	${OUTPUT_DIR}/Develop_Technical_Vision.pdf \
	${OUTPUT_DIR}/Glossary.pdf \
	${OUTPUT_DIR}/Index_over_dokument.pdf \
	${OUTPUT_DIR}/Iteration_plan_-_elaboration.pdf \
	${OUTPUT_DIR}/Iteration_plan_-_inception.pdf \
	${OUTPUT_DIR}/Project_plan.pdf \
	${OUTPUT_DIR}/Risk_List.pdf \
	${OUTPUT_DIR}/System-WideRequirements.pdf \
	${OUTPUT_DIR}/Use-case_Model.pdf \
	${OUTPUT_DIR}/Use-case.pdf \
	${OUTPUT_DIR}/Vision.pdf \
	${OUTPUT_DIR}/Work_items_list.pdf \
	movelogs

dirs:
	@mkdir -p ${OUTPUT_DIR}
	@mkdir -p ${LOG_DIR}

movelogs:
	@mv ${OUTPUT_DIR}/*.log ${LOG_DIR}/
	@mv ${OUTPUT_DIR}/*.aux ${LOG_DIR}/
	@mv ${OUTPUT_DIR}/*.toc ${LOG_DIR}/

${OUTPUT_DIR}/Architecture_Notebook.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Architecture Notebook.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Architecture Notebook.tex" > /dev/null

${OUTPUT_DIR}/Develop_Technical_Vision.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Develop Technical Vision.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Develop Technical Vision.tex" > /dev/null

${OUTPUT_DIR}/Glossary.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Glossary.tex
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Glossary.tex > /dev/null

${OUTPUT_DIR}/Index_over_dokument.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Index over dokument.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Index over dokument.tex" > /dev/null

${OUTPUT_DIR}/Iteration_plan_-_elaboration.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Iteration plan - elaboration.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Iteration plan - elaboration.tex" > /dev/null

${OUTPUT_DIR}/Iteration_plan_-_inception.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Iteration plan - inception.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Iteration plan - inception.tex" > /dev/null

# Kompilera denna två gånger för att få med referenser.
${OUTPUT_DIR}/Project_plan.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Project plan.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Project plan.tex" > /dev/null

${OUTPUT_DIR}/Risk_List.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Risk List.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Risk List.tex" > /dev/null

${OUTPUT_DIR}/System-WideRequirements.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ System-WideRequirements.tex
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ System-WideRequirements.tex > /dev/null

${OUTPUT_DIR}/Use-case_Model.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Use-case Model.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Use-case Model.tex" > /dev/null

${OUTPUT_DIR}/Use-case.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Use-case.tex
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Use-case.tex > /dev/null

${OUTPUT_DIR}/Vision.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Vision.tex
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Vision.tex > /dev/null

${OUTPUT_DIR}/Work_items_list.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Work items list.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Work items list.tex" > /dev/null

