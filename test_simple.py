#!/usr/bin/env python3
"""
簡單的 NBT 測試
"""

import sys
import os
import tempfile

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.nbt_types import NbtCompound, NbtInt, NbtString, NbtByte
from core.nbt_file import NbtFile

def test_simple_nbt():
    """測試簡單的 NBT 創建和讀取"""
    print("=== 測試簡單的 NBT 創建和讀取 ===")
    
    # 創建簡單的 NBT 數據
    root = NbtCompound({
        'Data': NbtCompound({
            'Player': NbtCompound({
                'GameType': NbtInt(0),
                'Level': NbtInt(1)
            })
        })
    })
    
    print("創建的 NBT 數據:")
    print(f"根標籤類型: {type(root).__name__}")
    print(f"Data 標籤類型: {type(root['Data']).__name__}")
    print(f"Player 標籤類型: {type(root['Data']['Player']).__name__}")
    print(f"GameType 值: {root['Data']['Player']['GameType']}")
    print(f"Level 值: {root['Data']['Player']['Level']}")
    
    # 創建 NBT 文件
    nbt_file = NbtFile(root, compression='none', little_endian=False, bedrock_header=False)
    
    # 寫入字節
    data = nbt_file.write()
    print(f"\n寫入的字節數: {len(data)}")
    print(f"字節數據 (前50字節): {data[:50]}")
    
    # 嘗試讀取
    try:
        read_file = NbtFile.read(data)
        print(f"\n讀取成功!")
        print(f"讀取的文件類型: {type(read_file.root).__name__}")
        print(f"壓縮: {read_file.compression}")
        print(f"字節序: {'little-endian' if read_file.little_endian else 'big-endian'}")
        print(f"Bedrock 頭部: {read_file.bedrock_header}")
        
        # 檢查數據
        if 'Data' in read_file.root:
            print("✅ Data 標籤讀取成功")
            if 'Player' in read_file.root['Data']:
                print("✅ Player 標籤讀取成功")
                if 'GameType' in read_file.root['Data']['Player']:
                    print("✅ GameType 標籤讀取成功")
                    print(f"GameType 值: {read_file.root['Data']['Player']['GameType']}")
                else:
                    print("❌ GameType 標籤讀取失敗")
            else:
                print("❌ Player 標籤讀取失敗")
        else:
            print("❌ Data 標籤讀取失敗")
            
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 測試完成 ===")

if __name__ == '__main__':
    test_simple_nbt()
