all: run_tests compile_report

run_tests:
	python3 src/ode_testing.py

compile_report:
	pdflatex -output-directory=report report/main.tex

clean:
	rm -f report/*.aux report/*.log report/*.pdf

