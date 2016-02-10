install:
	sudo apt-get install python-xlib gir1.2-appindicator3-0.1
	sudo apt-get install python3-pip
	sudo pip3 install ewmh
	sudo python setup.py install --prefix /usr

run:
	./caffeine-plus
