# .PHONY: apply를 추가하여 apply가 실제 파일이 아닌 타겟임을 명시
# .PHONY: apply

apply:
	cd app && ./build.sh && cd .. && cd infra && kubectl apply -f . && cd ..