################################################################################
# Copyright 2010 Andreas Neustifter (andreas.neustifter@gmail.com)
#
# This file is part of PhotoImport.
#
# PhotoImport is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PhotoImport is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PhotoImport. If not, see <http://www.gnu.org/licenses/>.
################################################################################

pylint: pylint.log

pylint.log: *.py Makefile pylint.rc pylint.whitelist
	@echo "--- Running pylint, pushing outout to $@"
	-pylint --rcfile pylint.rc *.py 2>&1 | grep -v -f pylint.whitelist > pylint.log

coverage:
	-python-coverage run -a PhotoImport.py
	-python-coverage annotate

coverage-report:
	-mkdir $@
	-python-coverage html -d $@

test:
	find Dest -type f -delete
	find Test -name PhotoImport.db -delete
	python PhotoImport.py

clean:
	@echo "Warning!"
	@echo "The following files and folders will be deleted:"
	@echo " *.orig, *~, Dest/* "
	@echo "The following commands will be executed:"
	@echo " git clean -x -f"
	@echo " find . -name PhotoImport.db -delete"
	@echo "To run use 'make clean-really'."

clean-really:
	rm -rf *.orig *~ Dest/*
	git clean -x -f
	find . -name PhotoImport.db -delete
