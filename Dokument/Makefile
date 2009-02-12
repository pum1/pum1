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
	@mv -f ${OUTPUT_DIR}/*.log ${LOG_DIR}/
	@mv -f ${OUTPUT_DIR}/*.aux ${LOG_DIR}/
	@mv -f ${OUTPUT_DIR}/*.toc ${LOG_DIR}/

${OUTPUT_DIR}/Architecture_Notebook.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Architecture Notebook.tex"

${OUTPUT_DIR}/Develop_Technical_Vision.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Develop Technical Vision.tex"

${OUTPUT_DIR}/Glossary.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Glossary.tex

${OUTPUT_DIR}/Index_over_dokument.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Index over dokument.tex"

${OUTPUT_DIR}/Iteration_plan_-_inception.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Iteration plan - inception.tex"

# Kompilera denna två gånger för att få med referenser.
${OUTPUT_DIR}/Project_plan.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Project plan.tex"
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Project plan.tex"

${OUTPUT_DIR}/Risk_List.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Risk List.tex"

${OUTPUT_DIR}/System-WideRequirements.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ System-WideRequirements.tex

${OUTPUT_DIR}/Use-case_Model.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Use-case Model.tex"

${OUTPUT_DIR}/Use-case.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Use-case.tex

${OUTPUT_DIR}/Vision.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ Vision.tex

${OUTPUT_DIR}/Work_items_list.pdf:
	${TEX_COMPILER} -output-directory ${OUTPUT_DIR}/ "Work items list.tex"

