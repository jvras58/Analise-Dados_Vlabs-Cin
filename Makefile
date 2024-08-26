SHEll := /bin/zsh
.PHONY: venv

venv:
	@poetry run poetry install


commit:
	@echo "Revisar mudanças para este commit: "
	@echo "-------------------------------------"
	@git status -s 
	@echo "-------------------------------------"
	@read -p "Commit msg: " menssagem ; \
	git add . ;\
	git commit -m "$$menssagem" ;\

update:
	@git fetch origin
	@git pull
	@$(MAKE) venv

run:
	@poetry run python src/data/make_dataset.py
	export PYTHONPATH=$$PYTHONPATH:/workspace/src && poetry run python src/features/build_features.py

start:
	@poetry run streamlit run src/visualization/visualize.py