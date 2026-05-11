IMAGE   := mcc
DATASETS ?= ./datasets

.PHONY: build run shell

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -v "$(DATASETS):/data" $(IMAGE) \
		python3 compare_all.py /data -o /data/results.csv $(ARGS)

shell:
	docker run --rm -it -v "$(DATASETS):/data" $(IMAGE)
