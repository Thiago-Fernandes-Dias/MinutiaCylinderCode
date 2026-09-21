IMAGE      := mcc
DATASETS   ?= ./datasets
SCORES_DIR ?= $(CURDIR)/../scores/MCC
OUTPUT_DIR ?= $(SCORES_DIR)

ifeq ($(wildcard $(DATASETS)/FVC_FingerNet_Artifacts),)
  ifneq ($(wildcard $(DATASETS)s/FVC_FingerNet_Artifacts),)
    override DATASETS := $(DATASETS)s
  endif
endif

.PHONY: build run shell

build:
	docker build -t $(IMAGE) .

run:
	mkdir -p "$(OUTPUT_DIR)"
	docker run --rm \
		-v "$(DATASETS):/Datasets" \
		-v "$(OUTPUT_DIR):/Scores" \
		-v "$(CURDIR)/compare_all.py:/app/compare_all.py" \
		$(IMAGE)

shell:
	mkdir -p "$(OUTPUT_DIR)"
	docker run --rm -it \
		-v "$(DATASETS):/Datasets" \
		-v "$(OUTPUT_DIR):/Scores" \
		-v "$(CURDIR)/compare_all.py:/app/compare_all.py" \
		$(IMAGE)
