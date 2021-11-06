run-fast: install-dependencies stop-existing-compose
	docker-compose -f docker-compose.fast.yml up -d

run-slow: install-dependencies stop-existing-compose
	docker-compose -f docker-compose.slow.yml up -d

stop-existing-compose:
	docker-compose -f docker-compose.slow.yml down
	docker-compose -f docker-compose.fast.yml down

install-dependencies:
	sudo apt-get install docker-ce
	sudo apt-get install docker-compose
