CXX      := mpic++
CXXFLAGS := -std=c++11 -O2 -Wall
INCLUDES := -I include -I MCC
BUILDDIR := build
TARGET   := mcc

SOURCES_COMMONS := Fingerprint.cpp Minutia.cpp Functions.cpp \
                   File19794.cpp Munkres.cpp GrahamScanConvexHull.cpp \
                   Score.cpp
SOURCES_MCC     := main.cpp MCC.cpp Cylinder.cpp

SRC_COMMONS := $(addprefix commons/,$(SOURCES_COMMONS))
SRC_MCC     := $(addprefix MCC/,$(SOURCES_MCC))
SOURCES     := $(SRC_COMMONS) $(SRC_MCC)

OBJECTS     := $(patsubst %.cpp,$(BUILDDIR)/%.o,$(SOURCES))

.PHONY: all clean check-deps

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(BUILDDIR)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(BUILDDIR) $(TARGET)

check-deps:
	@echo "=== Verificando dependencias ==="
	@echo ""
	@for tool in mpic++ g++; do \
		which $$tool >/dev/null 2>&1 && \
		echo "[OK] $$tool encontrado: $$($$tool --version 2>&1 | head -1)" || \
		echo "[FALTA] $$tool nao encontrado"; \
	done
	@echo ""
	@echo "=== MPI ==="
	@echo -n "mpi.h: "; \
	mpic++ -E -x c++ /dev/null -o /dev/null 2>/dev/null && echo "[OK]" || echo "[FALTA]"
	@echo ""
	@echo "=== Arquivos fonte ==="
	@missing=0; \
	for src in $(SRC_COMMONS) $(SRC_MCC); do \
		if [ -f "$$src" ]; then \
			echo "[OK] $$src"; \
		else \
			echo "[FALTA] $$src"; \
			missing=1; \
		fi; \
	done; \
	[ "$$missing" = "1" ] && echo "ERRO: Arquivos fonte faltando!" || true
