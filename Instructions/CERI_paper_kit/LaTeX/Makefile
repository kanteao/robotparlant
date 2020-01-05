main: template.tex
	mkdir -p obj/
	xelatex -halt-on-error -output-directory obj/  template.tex
	bibtex obj/template
	xelatex -halt-on-error -output-directory obj/ template.tex
	xelatex -halt-on-error -output-directory obj/ template.tex

clean:
	rm -rf obj/



