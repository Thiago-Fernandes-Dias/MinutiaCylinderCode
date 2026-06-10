IMAGE   := mcc
DATASETS ?= ./datasets
OUTPUT_DIR ?= ./output

.PHONY: build run shell

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -v "$(DATASETS):/Datasets" -v "$(OUTPUT_DIR):/Output" $(IMAGE)

shell:
	docker run --rm -it -v "$(DATASETS):/Datasets" -v "$(OUTPUT_DIR):/Output" $(IMAGE)
