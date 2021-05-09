 .PHONY: install
 install:
	sudo apt-get install build-essential python3-dev
	pip install -r database/requirements.txt

 .PHONY: run
run: install
	docker-compose up -d
	echo "Giving a time for docker to complete startup..." && sleep 3
	./database/setup_database.sh $(file)
	echo "Access the app at: http://127.0.0.1:4243"
