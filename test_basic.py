#!/usr/bin/env python3
"""
基本功能測試
測試 NBT 編輯器的核心功能
"""

import sys
import os

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.nbt_types import *
from core.nbt_path import NbtPath
from core.operations import *


def test_nbt_types():
    """測試 NBT 類型系統"""
    print("=== 測試 NBT 類型系統 ===")
    
    # 測試基本類型
    byte_tag = NbtByte(42)
    int_tag = NbtInt(12345)
    string_tag = NbtString("Hello World")
    float_tag = NbtFloat(3.14)
    
    print(f"Byte: {byte_tag} (類型: {byte_tag.type_id})")
    print(f"Int: {int_tag} (類型: {int_tag.type_id})")
    print(f"String: {string_tag} (類型: {string_tag.type_id})")
    print(f"Float: {float_tag} (類型: {float_tag.type_id})")
    
    # 測試數組類型
    byte_array = NbtByteArray([1, 2, 3, 4, 5])
    int_array = NbtIntArray([100, 200, 300])
    
    print(f"ByteArray: {byte_array}")
    print(f"IntArray: {int_array}")
    
    # 測試複合類型
    compound = NbtCompound({
        'name': NbtString("Test"),
        'value': NbtInt(42),
        'enabled': NbtByte(1)
    })
    
    print(f"Compound: {compound}")
    print(f"Compound keys: {list(compound.keys())}")
    
    # 測試列表類型
    list_tag = NbtList([
        NbtString("Item 1"),
        NbtString("Item 2"),
        NbtInt(100)
    ])
    
    print(f"List: {list_tag}")
    print(f"List element type: {list_tag.element_type}")
    
    print("✅ NBT 類型系統測試通過\n")


def test_nbt_path():
    """測試 NBT 路徑系統"""
    print("=== 測試 NBT 路徑系統 ===")
    
    # 測試路徑創建
    path1 = NbtPath("Data.Player.GameType")
    path2 = NbtPath(["Data", "Player", "GameType"])
    path3 = NbtPath("Data[0].Name")
    
    print(f"路徑1: {path1} -> {path1.arr}")
    print(f"路徑2: {path2} -> {path2.arr}")
    print(f"路徑3: {path3} -> {path3.arr}")
    
    # 測試路徑操作
    print(f"路徑1 頭部: {path1.head()}")
    print(f"路徑1 尾部: {path1.last()}")
    print(f"路徑1 長度: {path1.length()}")
    
    # 測試路徑修改
    new_path = path1.push("SubKey")
    print(f"添加子鍵後: {new_path}")
    
    parent_path = new_path.pop()
    print(f"移除子鍵後: {parent_path}")
    
    # 測試路徑比較
    print(f"路徑1 == 路徑2: {path1 == path2}")
    print(f"路徑1 以 Data 開頭: {path1.starts_with(NbtPath('Data'))}")
    
    print("✅ NBT 路徑系統測試通過\n")


def test_operations():
    """測試編輯操作系統"""
    print("=== 測試編輯操作系統 ===")
    
    # 創建測試數據
    root = NbtCompound({
        'Data': NbtCompound({
            'Player': NbtCompound({
                'GameType': NbtInt(0),
                'Level': NbtInt(1),
                'Inventory': NbtList([
                    NbtCompound({
                        'id': NbtString("minecraft:stone"),
                        'Count': NbtByte(64)
                    })
                ])
            })
        })
    })
    
    print("原始數據:")
    print_nbt_tree(root)
    
    # 測試設置操作
    print("\n--- 測試設置操作 ---")
    set_edit = NbtSetEdit("Data.Player.GameType", NbtInt(1))
    apply_edit_tag(root, set_edit)
    print("設置 GameType = 1 後:")
    print_nbt_tree(root)
    
    # 測試添加操作
    print("\n--- 測試添加操作 ---")
    add_edit = NbtAddEdit("Data.Player.Health", NbtFloat(20.0))
    apply_edit_tag(root, add_edit)
    print("添加 Health = 20.0 後:")
    print_nbt_tree(root)
    
    # 測試刪除操作
    print("\n--- 測試刪除操作 ---")
    remove_edit = NbtRemoveEdit("Data.Player.Level")
    apply_edit_tag(root, remove_edit)
    print("刪除 Level 後:")
    print_nbt_tree(root)
    
    # 測試搜索操作
    print("\n--- 測試搜索操作 ---")
    search_results = search_nodes(root, {'value': 'minecraft:stone'})
    print(f"搜索包含 'minecraft:stone' 的結果: {len(search_results)} 個")
    for result in search_results:
        print(f"  路徑: {result}")
    
    print("✅ 編輯操作系統測試通過\n")


def print_nbt_tree(tag, path="", max_depth=3, current_depth=0):
    """簡單的樹狀打印函數"""
    if current_depth >= max_depth:
        print("  " * current_depth + "... (max depth reached)")
        return
    
    if isinstance(tag, NbtCompound):
        for key, value in tag.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, (NbtCompound, NbtList)) and current_depth < max_depth - 1:
                print("  " * current_depth + f"📁 {key}:")
                print_nbt_tree(value, current_path, max_depth, current_depth + 1)
            else:
                print("  " * current_depth + f"📄 {key}: {value}")
    elif isinstance(tag, NbtList):
        for i, item in enumerate(tag._value):
            current_path = f"{path}[{i}]"
            if isinstance(item, (NbtCompound, NbtList)) and current_depth < max_depth - 1:
                print("  " * current_depth + f"📁 [{i}]:")
                print_nbt_tree(item, current_path, max_depth, current_depth + 1)
            else:
                print("  " * current_depth + f"📄 [{i}]: {item}")


def main():
    """主測試函數"""
    print("🚀 開始測試 Minecraft NBT 編輯器\n")
    
    try:
        test_nbt_types()
        test_nbt_path()
        test_operations()
        
        print("🎉 所有測試通過！")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
