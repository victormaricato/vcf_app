 .PHONY: run
run:
	docker-compose up -d
	echo "Giving a time for docker to complete startup..." && sleep 3
	./database/setup_database.sh database/data/sample.vcf.gz
