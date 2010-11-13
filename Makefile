pylint: pylint.log

pylint.log: *.py Makefile
	@echo "--- Running pylint, pushing outout to $@"
	-pylint --rcfile pylint.rc $+ 2>&1 | grep -v -f pylint.whitelist > pylint.log
