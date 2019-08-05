# Makefile

install:
	mkdir -p /usr/share/grimedit
	cp -r ./icons /usr/share/grimedit/
	chmod 644 /usr/share/grimedit/icons/*
	cp grimedit /usr/bin/
	chmod 755 /usr/bin/grimedit
uninstall:
	rm -rf /usr/share/grimedit
	rm /usr/bin/grimedit
