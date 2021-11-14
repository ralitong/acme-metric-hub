test:
	python3 acme_core_test.py
	python3 metric_core_test.py

docker-run-many: docker-stop
	sudo docker-compose -f docker-compose.many.yml -p manyacme up -d --build

docker-run-few: docker-stop
	sudo docker-compose -f docker-compose.few.yml -p fewacme up -d --build

docker-stop:
	sudo docker-compose -f docker-compose.many.yml -p manyacme down
	sudo docker-compose -f docker-compose.few.yml -p fewacme down

install-dependencies-debian:
	sudo apt-get install docker -y
	sudo apt-get install docker-compose -y
	sudo apt-get install python3 -y
	sudo apt-get install python3-pip -y
	sudo apt-get install python3-flask -y
	sudo apt-get install curl -y
	pip3 install -r requirements.txt

	sudo systemctl enable docker
	sudo systemctl start docker

install-dependencies-fedora:
	sudo yum install docker -y
	sudo yum install docker-compose -y
	sudo yum install python3 -y
	sudo yum install python3-pip -y
	sudo yum install python3-flask -y
	sudo yum install curl -y
	pip3 install -r requirements.txt

	sudo systemctl enable docker
	sudo systemctl start docker

run-metric-server:
	bash start_metric_server.sh

run-normal-server:
	bash start_normal_acme_server.sh

run-unusual-server:
	bash start_unusual_acme_server.sh

get-statistics:
	curl http://localhost:5000/process_statistics

get-outliers:
	curl http://localhost:5000/process_outliers


get-dynamic-statistics:
	curl http://localhost:5000/v2/process_statistics

get-dynamic-outliers:
	curl http://localhost:5000/v2/process_outliers

