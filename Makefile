docker-run-fast: stop-docker
	docker-compose -f docker-compose.fast.yml -p fastacme up -d

docker-run-slow: stop-docker
	docker-compose -f docker-compose.slow.yml -p slowacme up -d

stop-docker:
	docker-compose -f docker-compose.fast.yml -p fastacme down
	docker-compose -f docker-compose.slow.yml -p slowacme down

install-dependencies-debian:
	sudo apt-get install docker -y
	sudo apt-get install docker-compose -y
	sudo apt-get install python3 -y
	sudo apt-get install python3-pip -y
	sudo apt-get install python3-flask -y
	sudo apt-get install curl -y
	pip3 install -r requirements.txt

install-dependencies-fedora:
	sudo yum install docker -y
	sudo yum install docker-compose -y
	sudo yum install python3 -y
	sudo yum install python3-pip -y
	sudo yum install python3-flask -y
	sudo yum install curl -y
	pip3 install -r requirements.txt

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

