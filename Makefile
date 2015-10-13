README.rst: README.md
	pandoc $< -o $@ || cp $< $@
