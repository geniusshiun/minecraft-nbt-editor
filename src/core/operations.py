"""
NBT 編輯操作系統
實現 NBT 數據的增刪改查、移動等操作
"""

from typing import Any, Dict, List, Optional, Union, Tuple
from .nbt_types import NbtTag, NbtCompound, NbtList, NbtType, NbtString, create_tag
from .nbt_path import NbtPath


class NbtEdit:
    """NBT 編輯操作基類"""
    
    def __init__(self, edit_type: str):
        self.type = edit_type


class NbtSetEdit(NbtEdit):
    """設置值編輯操作"""
    
    def __init__(self, path: Union[str, List[Union[str, int]]], new_value: Any, old_value: Any = None):
        super().__init__('set')
        self.path = NbtPath(path) if not isinstance(path, NbtPath) else path
        self.new = new_value
        self.old = old_value


class NbtAddEdit(NbtEdit):
    """添加值編輯操作"""
    
    def __init__(self, path: Union[str, List[Union[str, int]]], value: Any):
        super().__init__('add')
        self.path = NbtPath(path) if not isinstance(path, NbtPath) else path
        self.value = value


class NbtRemoveEdit(NbtEdit):
    """刪除值編輯操作"""
    
    def __init__(self, path: Union[str, List[Union[str, int]]], value: Any = None):
        super().__init__('remove')
        self.path = NbtPath(path) if not isinstance(path, NbtPath) else path
        self.value = value


class NbtMoveEdit(NbtEdit):
    """移動值編輯操作"""
    
    def __init__(self, path: Union[str, List[Union[str, int]]], source: Union[str, List[Union[str, int]]]):
        super().__init__('move')
        self.path = NbtPath(path) if not isinstance(path, NbtPath) else path
        self.source = NbtPath(source) if not isinstance(source, NbtPath) else source


class NbtCompositeEdit(NbtEdit):
    """複合編輯操作，包含多個子編輯"""
    
    def __init__(self, edits: List[NbtEdit]):
        super().__init__('composite')
        self.edits = edits


def reverse_edit(edit: NbtEdit) -> NbtEdit:
    """
    反轉編輯操作
    
    Args:
        edit: 要反轉的編輯操作
        
    Returns:
        反轉後的編輯操作
    """
    if edit.type == 'composite':
        reversed_edits = [reverse_edit(e) for e in reversed(edit.edits)]
        return NbtCompositeEdit(reversed_edits)
    elif edit.type == 'set':
        return NbtSetEdit(edit.path, edit.old, edit.new)
    elif edit.type == 'add':
        return NbtRemoveEdit(edit.path, edit.value)
    elif edit.type == 'remove':
        return NbtAddEdit(edit.path, edit.value)
    elif edit.type == 'move':
        return NbtMoveEdit(edit.source, edit.path)
    else:
        raise ValueError(f"Unknown edit type: {edit.type}")


def map_edit(edit: NbtEdit, mapper) -> NbtEdit:
    """
    映射編輯操作
    
    Args:
        edit: 要映射的編輯操作
        mapper: 映射函數
        
    Returns:
        映射後的編輯操作
    """
    if edit.type == 'composite':
        mapped_edits = [map_edit(e, mapper) for e in edit.edits]
        return NbtCompositeEdit(mapped_edits)
    else:
        return mapper(edit)


def apply_edit_tag(tag: NbtTag, edit: NbtEdit, logger=None) -> None:
    """
    將編輯操作應用到 NBT 標籤
    
    Args:
        tag: 要編輯的 NBT 標籤
        edit: 編輯操作
        logger: 日誌記錄器
        
    Raises:
        ValueError: 如果編輯操作無效
    """
    if logger:
        logger.info(f"Applying edit {edit_to_string(edit)}")
    
    try:
        if edit.type == 'composite':
            for sub_edit in edit.edits:
                apply_edit_tag(tag, sub_edit, logger)
            return
        
        if edit.path.is_empty():
            raise ValueError("Cannot apply edit to the root")
        
        path = edit.path
        node = get_node(tag, path.pop())
        last = path.last()
        
        if edit.type == 'set':
            set_value(node, last, edit.new)
        elif edit.type == 'add':
            add_value(node, last, edit.value)
        elif edit.type == 'remove':
            remove_value(node, last)
        elif edit.type == 'move':
            if edit.source.is_empty():
                raise ValueError("Cannot move the root")
            source_path = edit.source
            source_node = get_node(tag, source_path.pop())
            source_last = source_path.last()
            move_node(node, last, source_node, source_last)
        else:
            raise ValueError(f"Unknown edit type: {edit.type}")
            
    except Exception as e:
        if logger:
            logger.error(f"Error applying edit to tag: {str(e)}")
        raise


def get_node(tag: NbtTag, path: NbtPath) -> NbtTag:
    """
    根據路徑獲取節點
    
    Args:
        tag: 根標籤
        path: 路徑
        
    Returns:
        找到的節點
        
    Raises:
        ValueError: 如果路徑無效
    """
    node = tag
    
    for element in path.arr:
        if isinstance(node, NbtCompound) and isinstance(element, str):
            if element not in node:
                raise ValueError(f"Invalid path {path}: key '{element}' not found")
            node = node[element]
        elif hasattr(node, '__getitem__') and isinstance(element, int):
            if not hasattr(node, '__len__') or element >= len(node):
                raise ValueError(f"Invalid path {path}: index {element} out of range")
            node = node[element]
        else:
            raise ValueError(f"Invalid path {path}: cannot access '{element}' in {type(node).__name__}")
    
    return node


def set_value(tag: NbtTag, last: Union[str, int], value: Any) -> None:
    """
    設置值
    
    Args:
        tag: 要設置的標籤
        last: 最後一個路徑元素
        value: 新值
        
    Raises:
        ValueError: 如果設置操作無效
    """
    if isinstance(tag, NbtCompound) and isinstance(last, str):
        if isinstance(value, NbtTag):
            tag.set(last, value)
        else:
            # 嘗試自動轉換為適當的 NBT 類型
            nbt_value = auto_convert_to_nbt(value)
            tag.set(last, nbt_value)
    elif isinstance(tag, NbtList) and isinstance(last, int):
        if isinstance(value, NbtTag):
            tag._value[last] = value
        else:
            nbt_value = auto_convert_to_nbt(value)
            tag._value[last] = nbt_value
    elif hasattr(tag, '_value') and isinstance(last, int):
        # 處理數組類型
        if isinstance(value, NbtTag):
            tag._value[last] = value.value
        else:
            tag._value[last] = value
    else:
        raise ValueError(f"Cannot set value in {type(tag).__name__} with key {last}")


def add_value(tag: NbtTag, last: Union[str, int], value: Any) -> None:
    """
    添加值
    
    Args:
        tag: 要添加的標籤
        last: 最後一個路徑元素
        value: 要添加的值
        
    Raises:
        ValueError: 如果添加操作無效
    """
    if isinstance(tag, NbtCompound) and isinstance(last, str):
        if isinstance(value, NbtTag):
            tag.set(last, value)
        else:
            nbt_value = auto_convert_to_nbt(value)
            tag.set(last, nbt_value)
    elif isinstance(tag, NbtList) and isinstance(last, int):
        if isinstance(value, NbtTag):
            tag._value.insert(last, value)
        else:
            nbt_value = auto_convert_to_nbt(value)
            tag._value.insert(last, nbt_value)
    elif hasattr(tag, '_value') and isinstance(last, int):
        # 處理數組類型
        if isinstance(value, NbtTag):
            tag._value.insert(last, value.value)
        else:
            tag._value.insert(last, value)
    else:
        raise ValueError(f"Cannot add value to {type(tag).__name__} with key {last}")


def remove_value(tag: NbtTag, last: Union[str, int]) -> None:
    """
    刪除值
    
    Args:
        tag: 要刪除的標籤
        last: 最後一個路徑元素
        
    Raises:
        ValueError: 如果刪除操作無效
    """
    if isinstance(tag, NbtCompound) and isinstance(last, str):
        tag.delete(last)
    elif hasattr(tag, '_value') and isinstance(last, int):
        del tag._value[last]
    else:
        raise ValueError(f"Cannot remove value from {type(tag).__name__} with key {last}")


def move_node(tag: NbtTag, last: Union[str, int], source_tag: NbtTag, source_last: Union[str, int]) -> None:
    """
    移動節點
    
    Args:
        tag: 目標標籤
        last: 目標路徑元素
        source_tag: 源標籤
        source_last: 源路徑元素
        
    Raises:
        ValueError: 如果移動操作無效
    """
    value = get_node(source_tag, NbtPath([source_last]))
    add_value(tag, last, value)
    remove_value(source_tag, source_last)


def auto_convert_to_nbt(value: Any) -> NbtTag:
    """
    自動將值轉換為適當的 NBT 類型
    
    Args:
        value: 要轉換的值
        
    Returns:
        轉換後的 NBT 標籤
    """
    if isinstance(value, NbtTag):
        return value
    elif isinstance(value, bool):
        return NbtByte(1 if value else 0)
    elif isinstance(value, int):
        if -128 <= value <= 127:
            return NbtByte(value)
        elif -32768 <= value <= 32767:
            return NbtShort(value)
        elif -2147483648 <= value <= 2147483647:
            return NbtInt(value)
        else:
            return NbtLong(value)
    elif isinstance(value, float):
        return NbtDouble(value)
    elif isinstance(value, str):
        return NbtString(value)
    elif isinstance(value, list):
        if not value:
            return NbtList()
        
        # 檢查列表元素類型
        first_element = auto_convert_to_nbt(value[0])
        element_type = first_element.type_id
        
        # 轉換所有元素
        nbt_elements = []
        for item in value:
            nbt_item = auto_convert_to_nbt(item)
            if nbt_item.type_id != element_type:
                raise ValueError(f"List elements must be of the same type, got {element_type} and {nbt_item.type_id}")
            nbt_elements.append(nbt_item)
        
        return NbtList(nbt_elements, element_type)
    elif isinstance(value, dict):
        nbt_dict = {}
        for key, val in value.items():
            if not isinstance(key, str):
                raise ValueError("Dictionary keys must be strings")
            nbt_dict[key] = auto_convert_to_nbt(val)
        return NbtCompound(nbt_dict)
    else:
        raise ValueError(f"Cannot convert {type(value).__name__} to NBT tag")


def edit_to_string(edit: NbtEdit) -> str:
    """
    將編輯操作轉換為字符串表示
    
    Args:
        edit: 編輯操作
        
    Returns:
        字符串表示
    """
    if edit.type == 'composite':
        return f"type={edit.type} edits={len(edit.edits)}"
    elif edit.type == 'set':
        value_str = str(edit.new)[:40]
        if len(str(edit.new)) > 40:
            value_str += "..."
        return f"type={edit.type} path={edit.path} value={value_str}"
    elif edit.type in ('add', 'remove'):
        value_str = str(edit.value)[:40]
        if len(str(edit.value)) > 40:
            value_str += "..."
        return f"type={edit.type} path={edit.path} value={value_str}"
    elif edit.type == 'move':
        return f"type={edit.type} path={edit.path} source={edit.source}"
    else:
        return f"type={edit.type}"


def search_nodes(tag: NbtCompound, query: Dict[str, Any]) -> List[NbtPath]:
    """
    搜索節點
    
    Args:
        tag: 要搜索的標籤
        query: 搜索查詢
        
    Returns:
        匹配的路徑列表
    """
    results = []
    search_nodes_impl(NbtPath(), tag, query, results)
    return results


def search_nodes_impl(path: NbtPath, tag: NbtTag, query: Dict[str, Any], results: List[NbtPath]) -> None:
    """
    遞歸搜索節點的實現
    
    Args:
        path: 當前路徑
        tag: 當前標籤
        query: 搜索查詢
        results: 結果列表
    """
    if matches_node(path, tag, query):
        results.append(path)
    
    if isinstance(tag, NbtCompound):
        for key in sorted(tag.keys()):
            search_nodes_impl(path.push(key), tag[key], query, results)
    elif isinstance(tag, NbtList):
        for i, item in enumerate(tag._value):
            search_nodes_impl(path.push(i), item, query, results)


def matches_node(path: NbtPath, tag: NbtTag, query: Dict[str, Any]) -> bool:
    """
    檢查節點是否匹配查詢條件
    
    Args:
        path: 節點路徑
        tag: 節點標籤
        query: 查詢條件
        
    Returns:
        如果匹配則返回 True
    """
    last = path.last()
    
    # 檢查類型
    if 'type' in query and tag.type_id != query['type']:
        return False
    
    # 檢查名稱
    if 'name' in query and (not isinstance(last, str) or query['name'] not in last):
        return False
    
    # 檢查值
    if 'value' in query:
        # 使用 type_id 來檢查類型，避免導入問題
        if tag.type_id == 8:  # NbtType.STRING
            return query['value'] in tag.value
        elif hasattr(tag, 'value'):
            return str(query['value']) in str(tag.value)
        return False
    
    return True
