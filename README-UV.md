# 使用 uv 安裝 Minecraft NBT Editor

這個專案現在支援使用 `uv` 進行依賴管理和安裝。

## 什麼是 uv？

`uv` 是一個快速的 Python 套件安裝器和解析器，由 Astral 開發。它比傳統的 pip 快很多，並且提供更好的依賴解析。

## 安裝 uv

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 使用 pip
```bash
pip install uv
```

## 快速開始

### 1. 安裝開發依賴
```bash
# 安裝所有開發依賴
uv pip install -r requirements-dev.txt

# 安裝專案（開發模式）
uv pip install -e .
```

### 2. 使用 Makefile 簡化操作
```bash
# 查看所有可用命令
make help

# 設置開發環境
make setup

# 安裝依賴
make install-dev

# 運行測試
make test

# 格式化代碼
make format

# 檢查代碼品質
make lint
```

### 3. 直接使用 uv 命令
```bash
# 安裝主要依賴
uv pip install -r requirements.txt

# 安裝開發依賴
uv pip install -r requirements-dev.txt

# 安裝專案
uv pip install -e .

# 運行測試
uv run pytest

# 格式化代碼
uv run black src/
```

## 專案結構

```
.
├── pyproject.toml          # 專案配置和依賴
├── requirements.txt        # 主要依賴
├── requirements-dev.txt    # 開發依賴
├── .python-version        # Python 版本
├── Makefile               # 常用命令
├── .pre-commit-config.yaml # 預提交檢查
└── src/                   # 源代碼
```

## 依賴管理

### 主要依賴
- `click`: 命令行界面
- `rich`: 豐富的終端輸出
- `tabulate`: 表格格式化

### 開發依賴
- `pytest`: 測試框架
- `pytest-cov`: 測試覆蓋率
- `black`: 代碼格式化
- `flake8`: 代碼檢查
- `mypy`: 類型檢查
- `pre-commit`: 預提交檢查
- `hatchling`: 建置後端

## 常用 uv 命令

```bash
# 創建虛擬環境
uv venv

# 激活虛擬環境
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 安裝套件
uv pip install package-name

# 安裝開發套件
uv pip install --dev package-name

# 更新套件
uv pip install --upgrade package-name

# 卸載套件
uv pip uninstall package-name

# 列出已安裝套件
uv pip list

# 檢查依賴
uv pip check
```

## 與傳統工具的比較

| 功能 | uv | pip | poetry |
|------|----|-----|---------|
| 安裝速度 | ⚡ 非常快 | 🐌 慢 | 🚀 快 |
| 依賴解析 | ✅ 優秀 | ⚠️ 基本 | ✅ 優秀 |
| 虛擬環境 | ✅ 內建 | ❌ 需 venv | ✅ 內建 |
| 鎖定檔案 | ✅ 自動 | ❌ 無 | ✅ 手動 |
| 相容性 | ✅ 高 | ✅ 最高 | ⚠️ 中等 |

## 故障排除

### 常見問題

1. **權限錯誤**
   ```bash
   # 使用 --user 標誌
   uv pip install --user package-name
   ```

2. **版本衝突**
   ```bash
   # 檢查依賴
   uv pip check
   
   # 重新安裝
   uv pip install --force-reinstall package-name
   ```

3. **虛擬環境問題**
   ```bash
   # 重新創建虛擬環境
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   ```

### 獲取幫助
```bash
uv --help
uv pip --help
uv venv --help
```

## 貢獻指南

1. Fork 專案
2. 創建功能分支
3. 安裝開發依賴：`make install-dev`
4. 運行測試：`make test`
5. 格式化代碼：`make format`
6. 提交變更
7. 發起 Pull Request

## 更多資源

- [uv 官方文檔](https://docs.astral.sh/uv/)
- [uv GitHub](https://github.com/astral-sh/uv)
- [Python 打包指南](https://packaging.python.org/) 