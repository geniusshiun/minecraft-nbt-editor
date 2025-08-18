"""
二進制操作工具
提供 NBT 文件二進制數據的處理功能
"""

import struct
from typing import Union, Tuple, List, Optional


def read_byte(data: bytes, offset: int, little_endian: bool = False) -> Tuple[int, int]:
    """
    讀取一個字節
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian（對字節無影響）
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset >= len(data):
        raise ValueError("Unexpected end of data")
    return data[offset], offset + 1


def read_short(data: bytes, offset: int, little_endian: bool = False) -> Tuple[int, int]:
    """
    讀取一個短整數
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset + 2 > len(data):
        raise ValueError("Unexpected end of data")
    
    format_char = '<h' if little_endian else '>h'
    value = struct.unpack(format_char, data[offset:offset+2])[0]
    return value, offset + 2


def read_int(data: bytes, offset: int, little_endian: bool = False) -> Tuple[int, int]:
    """
    讀取一個整數
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset + 4 > len(data):
        raise ValueError("Unexpected end of data")
    
    format_char = '<i' if little_endian else '>i'
    value = struct.unpack(format_char, data[offset:offset+4])[0]
    return value, offset + 4


def read_long(data: bytes, offset: int, little_endian: bool = False) -> Tuple[int, int]:
    """
    讀取一個長整數
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset + 8 > len(data):
        raise ValueError("Unexpected end of data")
    
    format_char = '<q' if little_endian else '>q'
    value = struct.unpack(format_char, data[offset:offset+8])[0]
    return value, offset + 8


def read_float(data: bytes, offset: int, little_endian: bool = False) -> Tuple[float, int]:
    """
    讀取一個浮點數
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset + 4 > len(data):
        raise ValueError("Unexpected end of data")
    
    format_char = '<f' if little_endian else '>f'
    value = struct.unpack(format_char, data[offset:offset+4])[0]
    return value, offset + 4


def read_double(data: bytes, offset: int, little_endian: bool = False) -> Tuple[float, int]:
    """
    讀取一個雙精度浮點數
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    if offset + 8 > len(data):
        raise ValueError("Unexpected end of data")
    
    format_char = '<d' if little_endian else '>d'
    value = struct.unpack(format_char, data[offset:offset+8])[0]
    return value, offset + 8


def read_string(data: bytes, offset: int, little_endian: bool = False) -> Tuple[str, int]:
    """
    讀取一個字符串
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    # 讀取字符串長度
    str_length, offset = read_short(data, offset, little_endian)
    
    if offset + str_length > len(data):
        raise ValueError("Unexpected end of data while reading string")
    
    # 讀取字符串內容
    value = data[offset:offset+str_length].decode('utf-8')
    return value, offset + str_length


def read_byte_array(data: bytes, offset: int, little_endian: bool = False) -> Tuple[List[int], int]:
    """
    讀取一個字節數組
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    # 讀取數組長度
    array_length, offset = read_int(data, offset, little_endian)
    
    if offset + array_length > len(data):
        raise ValueError("Unexpected end of data while reading byte array")
    
    # 讀取數組內容
    values = list(data[offset:offset+array_length])
    return values, offset + array_length


def read_int_array(data: bytes, offset: int, little_endian: bool = False) -> Tuple[List[int], int]:
    """
    讀取一個整數數組
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    # 讀取數組長度
    array_length, offset = read_int(data, offset, little_endian)
    
    if offset + array_length * 4 > len(data):
        raise ValueError("Unexpected end of data while reading int array")
    
    # 讀取數組內容
    format_char = f'<{array_length}i' if little_endian else f'>{array_length}i'
    values = list(struct.unpack(format_char, data[offset:offset+array_length*4]))
    return values, offset + array_length * 4


def read_long_array(data: bytes, offset: int, little_endian: bool = False) -> Tuple[List[int], int]:
    """
    讀取一個長整數數組
    
    Args:
        data: 字節數據
        offset: 當前偏移量
        little_endian: 是否使用 little-endian
        
    Returns:
        (值, 新偏移量) 元組
    """
    # 讀取數組長度
    array_length, offset = read_int(data, offset, little_endian)
    
    if offset + array_length * 8 > len(data):
        raise ValueError("Unexpected end of data while reading long array")
    
    # 讀取數組內容
    format_char = f'<{array_length}q' if little_endian else f'>{array_length}q'
    values = list(struct.unpack(format_char, data[offset:offset+array_length*8]))
    return values, offset + array_length * 8


def write_byte(value: int, little_endian: bool = False) -> bytes:
    """
    寫入一個字節
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian（對字節無影響）
        
    Returns:
        字節序列
    """
    return struct.pack('B', value & 0xFF)


def write_short(value: int, little_endian: bool = False) -> bytes:
    """
    寫入一個短整數
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    format_char = '<H' if little_endian else '>H'
    return struct.pack(format_char, value & 0xFFFF)


def write_int(value: int, little_endian: bool = False) -> bytes:
    """
    寫入一個整數
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    format_char = '<I' if little_endian else '>I'
    return struct.pack(format_char, value & 0xFFFFFFFF)


def write_long(value: int, little_endian: bool = False) -> bytes:
    """
    寫入一個長整數
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    format_char = '<Q' if little_endian else '>Q'
    return struct.pack(format_char, value & 0xFFFFFFFFFFFFFFFF)


def write_float(value: float, little_endian: bool = False) -> bytes:
    """
    寫入一個浮點數
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    format_char = '<f' if little_endian else '>f'
    return struct.pack(format_char, value)


def write_double(value: float, little_endian: bool = False) -> bytes:
    """
    寫入一個雙精度浮點數
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    format_char = '<d' if little_endian else '>d'
    return struct.pack(format_char, value)


def write_string(value: str, little_endian: bool = False) -> bytes:
    """
    寫入一個字符串
    
    Args:
        value: 要寫入的值
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    value_bytes = value.encode('utf-8')
    length_bytes = write_short(len(value_bytes), little_endian)
    return length_bytes + value_bytes


def write_byte_array(values: List[int], little_endian: bool = False) -> bytes:
    """
    寫入一個字節數組
    
    Args:
        values: 要寫入的值列表
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    length_bytes = write_int(len(values), little_endian)
    data_bytes = struct.pack(f'<{len(values)}B' if little_endian else f'>{len(values)}B', *values)
    return length_bytes + data_bytes


def write_int_array(values: List[int], little_endian: bool = False) -> bytes:
    """
    寫入一個整數數組
    
    Args:
        values: 要寫入的值列表
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    length_bytes = write_int(len(values), little_endian)
    data_bytes = struct.pack(f'<{len(values)}i' if little_endian else f'>{len(values)}i', *values)
    return length_bytes + data_bytes


def write_long_array(values: List[int], little_endian: bool = False) -> bytes:
    """
    寫入一個長整數數組
    
    Args:
        values: 要寫入的值列表
        little_endian: 是否使用 little-endian
        
    Returns:
        字節序列
    """
    length_bytes = write_int(len(values), little_endian)
    data_bytes = struct.pack(f'<{len(values)}q' if little_endian else f'>{len(values)}q', *values)
    return length_bytes + data_bytes


def detect_endianness(data: bytes, offset: int = 0) -> bool:
    """
    檢測數據的字節序
    
    Args:
        data: 字節數據
        offset: 開始檢測的偏移量
        
    Returns:
        如果檢測到 little-endian 則返回 True，否則返回 False
    """
    if len(data) < offset + 4:
        return False
    
    # 嘗試讀取一個整數，檢查是否為合理的值
    # 假設大多數 NBT 文件中的整數值不會太大
    big_endian_value = struct.unpack('>i', data[offset:offset+4])[0]
    little_endian_value = struct.unpack('<i', data[offset:offset+4])[0]
    
    # 如果 little-endian 值更合理（較小），則認為是 little-endian
    return abs(little_endian_value) < abs(big_endian_value)


def hex_dump(data: bytes, offset: int = 0, length: Optional[int] = None, bytes_per_line: int = 16) -> str:
    """
    生成十六進制轉儲
    
    Args:
        data: 要轉儲的數據
        offset: 開始偏移量
        length: 要轉儲的長度，如果為 None 則轉儲到末尾
        bytes_per_line: 每行顯示的字節數
        
    Returns:
        十六進制轉儲字符串
    """
    if length is None:
        length = len(data) - offset
    
    result = []
    for i in range(0, length, bytes_per_line):
        line_data = data[offset+i:offset+i+bytes_per_line]
        
        # 十六進制表示
        hex_part = ' '.join(f'{b:02x}' for b in line_data)
        hex_part = hex_part.ljust(bytes_per_line * 3 - 1)
        
        # ASCII 表示
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in line_data)
        
        # 偏移量
        offset_part = f'{offset+i:08x}'
        
        result.append(f'{offset_part}: {hex_part} |{ascii_part}|')
    
    return '\n'.join(result)
