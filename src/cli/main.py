"""
Minecraft NBT 編輯器命令行界面
提供完整的 NBT 文件編輯功能
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Any

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.text import Text

try:
    from ..core import (
        NbtFile, NbtCompound, NbtTag, NbtList, NbtPath, NbtByte,
        NbtSetEdit, NbtAddEdit, NbtRemoveEdit, NbtMoveEdit,
        read_nbt_file, write_nbt_file, detect_file_format,
        get_node, apply_edit_tag, search_nodes
    )
    from ..core.operations import auto_convert_to_nbt
    from ..utils.i18n import get_text
except (ImportError, ValueError):
    # 當作為 entry point 執行時，使用絕對導入
    from core import (
        NbtFile, NbtCompound, NbtTag, NbtList, NbtPath, NbtByte,
        NbtSetEdit, NbtAddEdit, NbtRemoveEdit, NbtMoveEdit,
        read_nbt_file, write_nbt_file, detect_file_format,
        get_node, apply_edit_tag, search_nodes
    )
    from core.operations import auto_convert_to_nbt
    from utils.i18n import get_text

console = Console()


def print_nbt_tree(tag: NbtTag, path: str = "", max_depth: int = 10, current_depth: int = 0):
    """遞歸打印 NBT 樹狀結構"""
    if current_depth >= max_depth:
        console.print(f"{'  ' * current_depth}... (max depth reached)")
        return
    
    if isinstance(tag, NbtCompound):
        for key, value in tag.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(value, (NbtCompound, NbtList)) and current_depth < max_depth - 1:
                console.print(f"{'  ' * current_depth}📁 {key}:")
                print_nbt_tree(value, current_path, max_depth, current_depth + 1)
            else:
                console.print(f"{'  ' * current_depth}📄 {key}: {value}")
    elif isinstance(tag, NbtList):
        for i, item in enumerate(tag._value):
            current_path = f"{path}[{i}]"
            if isinstance(item, (NbtCompound, NbtList)) and current_depth < max_depth - 1:
                console.print(f"{'  ' * current_depth}📁 [{i}]:")
                print_nbt_tree(item, current_path, max_depth, current_depth + 1)
            else:
                console.print(f"{'  ' * current_depth}📄 [{i}]: {item}")
    else:
        console.print(f"{'  ' * current_depth}📄 {tag}")


def print_nbt_table(tag: NbtTag, path: str = ""):
    """以表格形式打印 NBT 數據"""
    table = Table(title=f"NBT Data: {path}" if path else "NBT Data")
    table.add_column("Path", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Value", style="yellow")
    
    def add_rows(tag: NbtTag, current_path: str):
        if isinstance(tag, NbtCompound):
            for key, value in tag.items():
                new_path = f"{current_path}.{key}" if current_path else key
                if isinstance(value, (NbtCompound, NbtList)):
                    table.add_row(new_path, type(value).__name__, f"[{len(value)} items]")
                    add_rows(value, new_path)
                else:
                    table.add_row(new_path, type(value).__name__, str(value))
        elif isinstance(tag, NbtList):
            for i, item in enumerate(tag._value):
                new_path = f"{current_path}[{i}]"
                if isinstance(item, (NbtCompound, NbtList)):
                    table.add_row(new_path, type(item).__name__, f"[{len(item)} items]")
                    add_rows(item, new_path)
                else:
                    table.add_row(new_path, type(item).__name__, str(item))
    
    add_rows(tag, path)
    console.print(table)


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """Minecraft NBT 編輯器 - 支援 Java 和 Bedrock 版本"""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['tree', 'table', 'json']), default='tree', help='輸出格式')
@click.option('--max-depth', '-d', type=int, default=10, help='最大深度')
@click.option('--path', '-p', help='只顯示指定路徑的內容')
def view(file_path: str, format: str, max_depth: int, path: str):
    """查看 NBT 文件內容"""
    try:
        console.print(f"正在讀取文件: {file_path}")
        
        # 檢測文件格式
        format_info = detect_file_format(file_path)
        console.print(f"文件格式: {format_info}")
        
        # 讀取 NBT 文件
        nbt_file = read_nbt_file(file_path)
        console.print(f"文件類型: {type(nbt_file.root).__name__}")
        console.print(f"壓縮: {nbt_file.compression}")
        console.print(f"字節序: {'little-endian' if nbt_file.little_endian else 'big-endian'}")
        console.print(f"Bedrock 頭部: {nbt_file.bedrock_header}")
        
        # 如果指定了路徑，只顯示該路徑的內容
        if path:
            try:
                target_tag = get_node(nbt_file.root, NbtPath(path))
                console.print(f"\n路徑 {path} 的內容:")
                if format == 'tree':
                    print_nbt_tree(target_tag, path, max_depth)
                elif format == 'table':
                    print_nbt_table(target_tag, path)
                else:  # json
                    console.print_json(json.dumps(target_tag.to_json(), indent=2, ensure_ascii=False))
            except ValueError as e:
                console.print(f"❌ 錯誤: {e}", style="red")
                return
        else:
            # 顯示整個文件
            console.print(f"\n文件內容:")
            if format == 'tree':
                print_nbt_tree(nbt_file.root, "", max_depth)
            elif format == 'table':
                print_nbt_table(nbt_file.root)
            else:  # json
                console.print_json(json.dumps(nbt_file.to_json(), indent=2, ensure_ascii=False))
                
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--path', '-p', required=True, help='要獲取值的路徑')
def get(file_path: str, path: str):
    """獲取指定路徑的值"""
    try:
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        target_tag = get_node(nbt_file.root, NbtPath(path))
        console.print(f"路徑 {path} 的值:")
        console.print(f"類型: {type(target_tag).__name__}")
        console.print(f"值: {target_tag}")
        
        if hasattr(target_tag, 'to_json'):
            console.print(f"JSON: {json.dumps(target_tag.to_json(), indent=2, ensure_ascii=False)}")
            
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--path', '-p', required=True, help='要設置值的路徑')
@click.option('--value', '-v', required=True, help='新值')
@click.option('--type', '-t', help='值的類型 (自動檢測如果未指定)')
@click.option('--backup', '-b', is_flag=True, help='創建備份文件')
def set(file_path: str, path: str, value: str, type: Optional[str], backup: bool):
    """設置指定路徑的值"""
    try:
        if backup:
            backup_path = f"{file_path}.backup"
            console.print(f"創建備份: {backup_path}")
            import shutil
            shutil.copy2(file_path, backup_path)
        
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        # 解析路徑
        nbt_path = NbtPath(path)
        if nbt_path.is_empty():
            console.print("❌ 錯誤: 不能設置根路徑", style="red")
            return
        
        # 獲取父節點
        parent_path = nbt_path.pop()
        parent_tag = get_node(nbt_file.root, parent_path)
        last_element = nbt_path.last()
        
        # 創建編輯操作
        if type:
            # 根據指定類型創建標籤
            type_map = {
                'byte': 'NbtByte',
                'short': 'NbtShort', 
                'int': 'NbtInt',
                'long': 'NbtLong',
                'float': 'NbtFloat',
                'double': 'NbtDouble',
                'string': 'NbtString',
                'bool': 'NbtByte'
            }
            if type not in type_map:
                console.print(f"❌ 錯誤: 不支援的類型 {type}", style="red")
                return
            
            # 創建適當的標籤
            if type == 'bool':
                nbt_value = NbtByte(1 if value.lower() in ('true', '1', 'yes') else 0)
            else:
                tag_class = globals()[type_map[type]]
                nbt_value = tag_class(value)
        else:
            # 自動檢測類型
            nbt_value = auto_convert_to_nbt(value)
        
        # 應用編輯
        edit = NbtSetEdit(path, nbt_value)
        apply_edit_tag(nbt_file.root, edit)
        
        console.print(f"✅ 成功設置 {path} = {nbt_value}")
        
        # 寫入文件
        write_nbt_file(file_path, nbt_file)
        console.print(f"✅ 文件已保存: {file_path}")
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--path', '-p', required=True, help='要添加標籤的路徑')
@click.option('--value', '-v', required=True, help='要添加的值')
@click.option('--type', '-t', help='值的類型 (自動檢測如果未指定)')
@click.option('--backup', '-b', is_flag=True, help='創建備份文件')
def add(file_path: str, path: str, value: str, type: Optional[str], backup: bool):
    """在指定路徑添加新的標籤"""
    try:
        if backup:
            backup_path = f"{file_path}.backup"
            console.print(f"創建備份: {backup_path}")
            import shutil
            shutil.copy2(file_path, backup_path)
        
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        # 解析路徑
        nbt_path = NbtPath(path)
        if nbt_path.is_empty():
            console.print("❌ 錯誤: 不能添加根路徑", style="red")
            return
        
        # 創建值
        if type:
            # 根據指定類型創建標籤
            type_map = {
                'byte': 'NbtByte',
                'short': 'NbtShort', 
                'int': 'NbtInt',
                'long': 'NbtLong',
                'float': 'NbtFloat',
                'double': 'NbtDouble',
                'string': 'NbtString',
                'bool': 'NbtByte'
            }
            if type not in type_map:
                console.print(f"❌ 錯誤: 不支援的類型 {type}", style="red")
                return
            
            if type == 'bool':
                nbt_value = NbtByte(1 if value.lower() in ('true', '1', 'yes') else 0)
            else:
                tag_class = globals()[type_map[type]]
                nbt_value = tag_class(value)
        else:
            # 自動檢測類型
            nbt_value = auto_convert_to_nbt(value)
        
        # 應用編輯
        edit = NbtAddEdit(path, nbt_value)
        apply_edit_tag(nbt_file.root, edit)
        
        console.print(f"✅ 成功添加 {path} = {nbt_value}")
        
        # 寫入文件
        write_nbt_file(file_path, nbt_file)
        console.print(f"✅ 文件已保存: {file_path}")
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--path', '-p', required=True, help='要刪除標籤的路徑')
@click.option('--backup', '-b', is_flag=True, help='創建備份文件')
def remove(file_path: str, path: str, backup: bool):
    """刪除指定路徑的標籤"""
    try:
        if backup:
            backup_path = f"{file_path}.backup"
            console.print(f"創建備份: {backup_path}")
            import shutil
            shutil.copy2(file_path, backup_path)
        
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        # 解析路徑
        nbt_path = NbtPath(path)
        if nbt_path.is_empty():
            console.print("❌ 錯誤: 不能刪除根路徑", style="red")
            return
        
        # 獲取要刪除的值（用於顯示）
        try:
            old_value = get_node(nbt_file.root, nbt_path)
            console.print(f"將要刪除: {path} = {old_value}")
        except ValueError:
            console.print(f"❌ 錯誤: 路徑 {path} 不存在", style="red")
            return
        
        # 應用編輯
        edit = NbtRemoveEdit(path)
        apply_edit_tag(nbt_file.root, edit)
        
        console.print(f"✅ 成功刪除 {path}")
        
        # 寫入文件
        write_nbt_file(file_path, nbt_file)
        console.print(f"✅ 文件已保存: {file_path}")
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--query', '-q', help='搜索查詢 (JSON 格式)')
@click.option('--type', '-t', type=int, help='標籤類型')
@click.option('--name', '-n', help='標籤名稱包含的字符串')
@click.option('--value', '-v', help='標籤值包含的字符串')
def search(file_path: str, query: Optional[str], type: Optional[int], name: Optional[str], search_value: Optional[str]):
    """搜索 NBT 文件中的標籤"""
    try:
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        # 構建搜索查詢
        search_query = {}
        if query:
            try:
                search_query = json.loads(query)
            except json.JSONDecodeError:
                console.print("❌ 錯誤: 無效的 JSON 查詢", style="red")
                return
        
        if type is not None:
            search_query['type'] = type
        if name:
            search_query['name'] = name
        if search_value:
            search_query['value'] = search_value
        
        if not search_query:
            console.print("❌ 錯誤: 必須指定至少一個搜索條件", style="red")
            return
        
        console.print(f"搜索查詢: {search_query}")
        
        # 執行搜索
        results = search_nodes(nbt_file.root, search_query)
        
        if not results:
            console.print("🔍 沒有找到匹配的結果")
            return
        
        console.print(f"🔍 找到 {len(results)} 個匹配結果:")
        
        # 顯示結果
        table = Table(title="搜索結果")
        table.add_column("路徑", style="cyan")
        table.add_column("值", style="yellow")
        
        for result_path in results:
            try:
                value = get_node(nbt_file.root, result_path)
                table.add_row(str(result_path), str(value))
            except ValueError:
                table.add_row(str(result_path), "[無法獲取值]")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='輸出文件路徑')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml']), default='json', help='輸出格式')
@click.option('--pretty', '-p', is_flag=True, help='美化輸出')
def convert(file_path: str, output: str, format: str, pretty: bool):
    """轉換 NBT 文件為其他格式"""
    try:
        console.print(f"正在讀取文件: {file_path}")
        nbt_file = read_nbt_file(file_path)
        
        if format == 'json':
            data = nbt_file.to_json()
            if pretty:
                output_data = json.dumps(data, indent=2, ensure_ascii=False)
            else:
                output_data = json.dumps(data, ensure_ascii=False)
        elif format == 'yaml':
            try:
                import yaml
                data = nbt_file.to_json()
                output_data = yaml.dump(data, default_flow_style=False, allow_unicode=True)
            except ImportError:
                console.print("❌ 錯誤: 需要安裝 PyYAML 來支援 YAML 輸出", style="red")
                return
        
        # 寫入輸出文件
        with open(output, 'w', encoding='utf-8') as f:
            f.write(output_data)
        
        console.print(f"✅ 成功轉換為 {format.upper()} 格式: {output}")
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--exp', '--experiments', is_flag=True, help='啟用所有實驗性功能')
@click.option('--backup', '-b', is_flag=True, help='創建備份文件')
def enable(file_path: str, exp: bool, backup: bool):
    """啟用 Minecraft 世界的各種功能"""
    if not exp:
        console.print(get_text("enable.specify_option"), style="red")
        console.print(get_text("enable.available_options"))
        console.print(get_text("enable.exp_option"))
        sys.exit(1)
    
    try:
        # 創建備份
        if backup:
            backup_path = f"{file_path}.backup"
            import shutil
            shutil.copy2(file_path, backup_path)
            console.print(get_text("enable.backup_created", backup_path), style="green")
        
        if exp:
            console.print(get_text("enable.enabling_experiments"))
            
            # 定義所有實驗性功能
            experiments = {
                "data_driven_biomes": 1,
                "experimental_creator_cameras": 1,
                "experiments_ever_used": 1,
                "gametest": 1,
                "jigsaw_structures": 1,
                "saved_with_toggled_experiments": 1,
                "upcoming_creator_features": 1,
                "villager_trades_rebalance": 1,
                "y_2025_drop_3": 1
            }
            
            # 讀取檔案
            nbt_file = read_nbt_file(file_path)
            
            # 檢查是否存在 experiments 標籤
            experiments_path = NbtPath("experiments")
            
            try:
                experiments_tag = get_node(nbt_file.root, experiments_path)
                if not isinstance(experiments_tag, NbtCompound):
                    # 如果 experiments 不是 compound，創建新的
                    experiments_tag = NbtCompound({})
                    edit = NbtSetEdit(experiments_path, experiments_tag)
                    apply_edit_tag(nbt_file.root, edit)
            except:
                # experiments 標籤不存在，創建新的
                experiments_tag = NbtCompound({})
                edit = NbtSetEdit(experiments_path, experiments_tag)
                apply_edit_tag(nbt_file.root, edit)
            
            # 設置每個實驗性功能
            for exp_name, exp_value in experiments.items():
                exp_path = NbtPath(f"experiments.{exp_name}")
                exp_byte = NbtByte(exp_value)
                edit = NbtSetEdit(exp_path, exp_byte)
                apply_edit_tag(nbt_file.root, edit)
                console.print(get_text("enable.feature_enabled", exp_name, exp_value))
            
            # 寫入檔案
            write_nbt_file(file_path, nbt_file)
            
            console.print(get_text("enable.all_enabled"), style="green")
            console.print(get_text("enable.restart_hint"), style="yellow")
            
    except Exception as e:
        console.print(get_text("error", str(e)), style="red")
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def info(file_path: str):
    """顯示 NBT 文件信息"""
    try:
        console.print(f"正在分析文件: {file_path}")
        
        # 檢測文件格式
        format_info = detect_file_format(file_path)
        
        # 獲取文件大小
        file_size = os.path.getsize(file_path)
        
        # 嘗試讀取 NBT 文件
        try:
            nbt_file = read_nbt_file(file_path)
            nbt_info = {
                'root_type': type(nbt_file.root).__name__,
                'compression': nbt_file.compression,
                'little_endian': nbt_file.little_endian,
                'bedrock_header': nbt_file.bedrock_header
            }
        except Exception as e:
            nbt_info = {'error': str(e)}
        
        # 顯示信息
        table = Table(title="文件信息")
        table.add_column("屬性", style="cyan")
        table.add_column("值", style="yellow")
        
        table.add_row("文件路徑", file_path)
        table.add_row("文件大小", f"{file_size} bytes")
        table.add_row("壓縮類型", format_info['compression'])
        table.add_row("字節序", "little-endian" if format_info['little_endian'] else "big-endian")
        table.add_row("Bedrock 頭部", str(format_info['bedrock_header']))
        
        if 'error' not in nbt_info:
            table.add_row("根標籤類型", nbt_info['root_type'])
            table.add_row("NBT 壓縮", nbt_info['compression'])
            table.add_row("NBT 字節序", "little-endian" if nbt_info['little_endian'] else "big-endian")
            table.add_row("NBT Bedrock 頭部", str(nbt_info['bedrock_header']))
        else:
            table.add_row("NBT 讀取錯誤", nbt_info['error'])
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ 錯誤: {e}", style="red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
