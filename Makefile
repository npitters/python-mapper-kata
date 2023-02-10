# All our targets are phony (no files to check), so performance should increase if implicit rule search is skipped.
.PHONY: unit_tests run
clean:
	./bin/clean.sh
unit_tests:
	./bin/unit_tests.sh
run:
	@./bin/run.sh $(file)
