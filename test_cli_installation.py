#!/usr/bin/env python3
"""
測試 CLI 安裝是否正確
"""

import subprocess
import sys
import os

def test_cli_installation():
    """測試 CLI 命令是否可用"""
    print("🧪 測試 CLI 安裝...")
    
    # 測試命令列表
    commands = [
        "minecraft-nbt --help",
        "nbt-editor --help",
        "minecraft-nbt --version",
        "nbt-editor --version"
    ]
    
    for cmd in commands:
        print(f"\n📋 測試命令: {cmd}")
        try:
            result = subprocess.run(
                cmd.split(), 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ 成功: {cmd}")
                if "help" in cmd:
                    print("   輸出預覽:")
                    lines = result.stdout.strip().split('\n')[:5]
                    for line in lines:
                        print(f"   {line}")
                    if len(result.stdout.strip().split('\n')) > 5:
                        print("   ...")
            else:
                print(f"❌ 失敗: {cmd}")
                print(f"   錯誤: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ 超時: {cmd}")
        except FileNotFoundError:
            print(f"🚫 命令未找到: {cmd}")
        except Exception as e:
            print(f"💥 異常: {cmd} - {e}")
    
    print("\n🔍 檢查 Python 路徑...")
    try:
        result = subprocess.run(
            ["which", "python3"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            python_path = result.stdout.strip()
            print(f"   Python3 路徑: {python_path}")
            
            # 檢查 site-packages
            result = subprocess.run(
                [python_path, "-c", "import site; print(site.getsitepackages())"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"   Site-packages: {result.stdout.strip()}")
        else:
            print("   Python3 未找到")
    except Exception as e:
        print(f"   檢查 Python 路徑時出錯: {e}")
    
    print("\n🔍 檢查已安裝的套件...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            minecraft_packages = [pkg for pkg in packages if "minecraft" in pkg.lower()]
            if minecraft_packages:
                print("   找到 Minecraft 相關套件:")
                for pkg in minecraft_packages:
                    print(f"     {pkg}")
            else:
                print("   未找到 Minecraft 相關套件")
        else:
            print(f"   檢查套件時出錯: {result.stderr}")
    except Exception as e:
        print(f"   檢查套件時出錯: {e}")

def test_import():
    """測試模組導入"""
    print("\n🧪 測試模組導入...")
    
    modules_to_test = [
        "src.cli.main",
        "src.core",
        "click",
        "rich"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ 成功導入: {module}")
        except ImportError as e:
            print(f"❌ 導入失敗: {module} - {e}")
        except Exception as e:
            print(f"💥 導入異常: {module} - {e}")

if __name__ == "__main__":
    print("🚀 Minecraft NBT Editor CLI 安裝測試")
    print("=" * 50)
    
    test_import()
    test_cli_installation()
    
    print("\n" + "=" * 50)
    print("✨ 測試完成！")
    
    print("\n📝 如果 CLI 命令不可用，請嘗試:")
    print("   1. 重新安裝: uv pip install -e .")
    print("   2. 檢查 PATH: echo $PATH")
    print("   3. 檢查虛擬環境: which python")
    print("   4. 使用完整路徑: python -m src.cli.main --help") 