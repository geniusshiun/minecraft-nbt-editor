#!/usr/bin/env python3
"""
自動化建立 release 和 dist 的腳本
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, description):
    """執行命令並處理錯誤"""
    print(f"🔄 {description}...")
    print(f"   執行: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        if result.stdout.strip():
            print(f"   輸出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗")
        print(f"   錯誤碼: {e.returncode}")
        if e.stderr:
            print(f"   錯誤: {e.stderr}")
        return False

def clean_build():
    """清理舊的建置檔案"""
    print("🧹 清理舊的建置檔案...")
    
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        if '*' in pattern:
            # 處理萬用字元
            for item in Path('.').glob(pattern):
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                    print(f"   刪除目錄: {item}")
                else:
                    item.unlink(missing_ok=True)
                    print(f"   刪除檔案: {item}")
        else:
            path = Path(pattern)
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                    print(f"   刪除目錄: {path}")
                else:
                    path.unlink(missing_ok=True)
                    print(f"   刪除檔案: {path}")

def build_package():
    """建置 Python 套件"""
    print("🔨 建置 Python 套件...")
    
    # 使用 uv 建置
    if run_command("uv build", "建置套件"):
        print("✅ 套件建置完成")
        return True
    else:
        print("❌ 套件建置失敗")
        return False

def check_dist_files():
    """檢查 dist 目錄中的檔案"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist 目錄不存在")
        return False
    
    files = list(dist_dir.glob("*"))
    if not files:
        print("❌ dist 目錄為空")
        return False
    
    print(f"📦 找到 {len(files)} 個分發檔案:")
    for file in files:
        size = file.stat().st_size
        print(f"   {file.name} ({size:,} bytes)")
    
    return True

def create_github_release_notes():
    """建立 GitHub Release 說明"""
    print("📝 建立 GitHub Release 說明...")
    
    # 讀取 CHANGELOG.md
    changelog_file = Path("CHANGELOG.md")
    if changelog_file.exists():
        with open(changelog_file, 'r', encoding='utf-8') as f:
            changelog = f.read()
        
        # 提取最新版本資訊
        lines = changelog.split('\n')
        release_notes = []
        in_version = False
        
        for line in lines:
            if line.startswith('## '):
                if in_version:
                    break
                if '0.2.0' in line or 'Unreleased' in line:
                    in_version = True
                    release_notes.append(line)
            elif in_version and line.strip():
                release_notes.append(line)
        
        if release_notes:
            release_content = '\n'.join(release_notes)
            with open("RELEASE_NOTES.md", 'w', encoding='utf-8') as f:
                f.write(release_content)
            print("✅ Release 說明已建立: RELEASE_NOTES.md")
            print("   內容預覽:")
            for line in release_content.split('\n')[:10]:
                print(f"   {line}")
            return True
    
    print("⚠️  未找到 CHANGELOG.md，請手動建立 Release 說明")
    return False

def main():
    """主函數"""
    print("🚀 Minecraft NBT Editor - Release 建置腳本")
    print("=" * 50)
    
    # 檢查必要工具
    if not shutil.which("uv"):
        print("❌ 未找到 uv，請先安裝: curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    if not shutil.which("git"):
        print("❌ 未找到 git")
        sys.exit(1)
    
    # 檢查 git 狀態
    if run_command("git status --porcelain", "檢查 git 狀態"):
        print("⚠️  工作目錄有未提交的變更，建議先提交或 stash")
    
    # 清理舊檔案
    clean_build()
    
    # 建置套件
    if not build_package():
        print("❌ 建置失敗，請檢查錯誤訊息")
        sys.exit(1)
    
    # 檢查 dist 檔案
    if not check_dist_files():
        print("❌ dist 檔案檢查失敗")
        sys.exit(1)
    
    # 建立 Release 說明
    create_github_release_notes()
    
    print("\n" + "=" * 50)
    print("🎉 建置完成！")
    print("\n📋 下一步:")
    print("   1. 檢查 dist/ 目錄中的檔案")
    print("   2. 在 GitHub 上建立新的 Release")
    print("   3. 上傳 dist/ 目錄中的檔案")
    print("   4. 複製 RELEASE_NOTES.md 的內容到 Release 說明")
    
    print("\n🔗 建立 GitHub Release:")
    print("   1. 前往: https://github.com/geniusshiun/minecraft-nbt-editor/releases")
    print("   2. 點擊 'Create a new release'")
    print("   3. 選擇 tag (例如: v0.2.0)")
    print("   4. 填寫標題和說明")
    print("   5. 上傳 dist/ 目錄中的檔案")
    print("   6. 發布 Release")

if __name__ == "__main__":
    main() 