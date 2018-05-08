TARGETS = python javascript java

all:
	$(foreach var,$(TARGETS),make -C $(var) all;)
clean:
	$(foreach var,$(TARGETS),make -C $(var) clean;)
