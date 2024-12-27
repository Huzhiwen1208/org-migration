.PHONY: clone
clone:
	@python3 clone.py

.PHONY: delete
delete:
	@chmod +x delete.sh
	@./delete.sh

.PHONY: push
push: delete
	@python3 push.py
