# Minecraft NBT 編輯器 Makefile

.PHONY: help install install-dev test test-cov lint format clean build install-cli demo test-basic create-example

help:  ## 顯示幫助信息
	@echo "Minecraft NBT 編輯器 - 可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安裝依賴
	pip3 install -r requirements.txt

install-dev:  ## 安裝開發依賴
	pip3 install -e ".[dev]"

test:  ## 運行測試
	python3 -m pytest tests/ -v

test-cov:  ## 運行測試並生成覆蓋率報告
	python3 -m pytest tests/ --cov=src --cov-report=html --cov-report=term

test-basic:  ## 運行基本功能測試
	python3 test_basic.py

lint:  ## 運行代碼檢查
	flake8 src/ tests/
	mypy src/

format:  ## 格式化代碼
	black src/ tests/
	isort src/ tests/

clean:  ## 清理生成的文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf build/ dist/

build:  ## 構建分發包
	python3 setup.py sdist bdist_wheel

install-cli:  ## 安裝命令行工具
	pip3 install -e .

demo:  ## 運行完整演示
	@echo "🚀 運行 Minecraft NBT 編輯器演示"
	@echo ""
	@echo "1. 創建示例文件..."
	@python3 -c "from src.core import NbtCompound, NbtInt, NbtString, NbtByte; import tempfile; root = NbtCompound({'Data': NbtCompound({'Player': NbtCompound({'GameType': NbtInt(0), 'Level': NbtInt(1), 'Health': NbtInt(20)})})}); f = tempfile.NamedTemporaryFile(mode='wb', suffix='.dat', delete=False); f.close(); from src.core.nbt_file import NbtFile; nbt_file = NbtFile(root); open(f.name, 'wb').write(nbt_file.write()); print(f'示例文件: {f.name}')"
	@echo ""
	@echo "2. 查看文件信息..."
	@python3 -m src.cli.main info /tmp/temp.dat 2>/dev/null || echo "請先創建示例文件"
	@echo ""
	@echo "3. 查看文件內容..."
	@python3 -m src.cli.main view /tmp/temp.dat 2>/dev/null || echo "請先創建示例文件"
	@echo ""
	@echo "4. 修改遊戲模式..."
	@python3 -m src.cli.main set /tmp/temp.dat --path Data.Player.GameType --value 1 2>/dev/null || echo "請先創建示例文件"
	@echo ""
	@echo "5. 查看修改後的內容..."
	@python3 -m src.cli.main view /tmp/temp.dat 2>/dev/null || echo "請先創建示例文件"
	@echo ""
	@echo "🎉 演示完成！"

create-example:  ## 創建示例 NBT 文件
	@echo "創建示例 NBT 文件..."
	@python3 -c "from src.core import NbtCompound, NbtInt, NbtString, NbtByte; import tempfile; root = NbtCompound({'Data': NbtCompound({'Player': NbtCompound({'GameType': NbtInt(0), 'Level': NbtInt(1), 'Health': NbtInt(20), 'FoodLevel': NbtInt(20), 'Experience': NbtInt(0), 'Inventory': NbtCompound({'Slot0': NbtCompound({'id': NbtString('minecraft:stone'), 'Count': NbtByte(64)})})})})}); f = tempfile.NamedTemporaryFile(mode='wb', suffix='.dat', delete=False); f.close(); from src.core.nbt_file import NbtFile; nbt_file = NbtFile(root); open(f.name, 'wb').write(nbt_file.write()); print(f'示例文件已創建: {f.name}'); print('使用以下命令查看文件內容:'); print(f'python3 -m src.cli.main view {f.name}'); print(f'python3 -m src.cli.main get {f.name} --path Data.Player.GameType'); print(f'python3 -m src.cli.main set {f.name} --path Data.Player.GameType --value 1'); print(f'python3 -m src.cli.main view {f.name}'); print(f'\\n清理臨時文件: rm {f.name}')"

.DEFAULT_GOAL := help
