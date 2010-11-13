pylint: pylint.log

pylint.log: *.py Makefile pylint.rc pylint.whitelist
	@echo "--- Running pylint, pushing outout to $@"
	-pylint --rcfile pylint.rc *.py 2>&1 | grep -v -f pylint.whitelist > pylint.log
