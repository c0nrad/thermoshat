deploy:
	git rev-parse HEAD > GIT_VERSION
	scp -r ./* pi@192.168.1.15:~/thermoshat

	# ssh pi@192.168.1.15 python3 wilfred.py

ssh:
	ssh pi@192.168.1.15

run:
	python3 thermoshat.py