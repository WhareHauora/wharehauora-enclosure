# explicit wildcard expansion suppresses errors when no files are found
include $(wildcard *.deps)

%.py:
	echo "import solid as s" > $@
	echo "import solid.utils as u" >> $@
	echo "s.scad_render_to_file(final, __file__.replace('.py', '.scad'))" >> $@

%.scad: %.py
	python $<

%.stl: %.scad
	openscad -m make -o $@ -d $@.deps $<

%.x3g: %.gcode
	gpx -g -p -m r1d $< $@

clean_stl:
	rm -f *.stl

clean_x3g:
	rm -f *.x3g
