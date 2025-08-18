"""
NBT 文件讀寫系統
支援多種 NBT 文件格式，包括 Bedrock Minecraft 的 little-endian 格式
"""

import struct
import gzip
import zlib
from typing import Any, Dict, List, Optional, Union, BinaryIO, Tuple
from .nbt_types import (
    NbtTag, NbtCompound, NbtList, NbtByte, NbtShort, NbtInt, NbtLong,
    NbtFloat, NbtDouble, NbtString, NbtByteArray, NbtIntArray, NbtLongArray,
    NbtEnd, NbtType, create_tag
)


class NbtFile:
    """NBT 文件類，支援讀取和寫入 NBT 文件"""
    
    def __init__(self, root: NbtCompound = None, compression: str = 'gzip', little_endian: bool = False, bedrock_header: bool = False):
        """
        初始化 NBT 文件
        
        Args:
            root: 根標籤，預設為空的複合標籤
            compression: 壓縮類型 ('gzip', 'zlib', 'none')
            little_endian: 是否使用 little-endian 字節序
            bedrock_header: 是否包含 Bedrock 頭部
        """
        self.root = root if root is not None else NbtCompound()
        self.compression = compression
        self.little_endian = little_endian
        self.bedrock_header = bedrock_header
    
    @classmethod
    def read(cls, data: Union[bytes, BinaryIO], compression: Optional[str] = None, 
             little_endian: Optional[bool] = None, bedrock_header: Optional[bool] = None) -> 'NbtFile':
        """
        從字節數據或文件讀取 NBT 文件
        
        Args:
            data: 字節數據或文件對象
            compression: 壓縮類型，如果為 None 則自動檢測
            little_endian: 字節序，如果為 None 則自動檢測
            bedrock_header: 是否包含 Bedrock 頭部，如果為 None 則自動檢測
            
        Returns:
            NbtFile 實例
            
        Raises:
            ValueError: 如果文件格式無效
        """
        if isinstance(data, bytes):
            file_data = data
        else:
            file_data = data.read()
        
        # 自動檢測壓縮類型
        if compression is None:
            if file_data.startswith(b'\x1f\x8b'):
                compression = 'gzip'
            elif file_data.startswith(b'\x78\x9c') or file_data.startswith(b'\x78\xda'):
                compression = 'zlib'
            else:
                compression = 'none'
        
        # 解壓縮
        if compression == 'gzip':
            try:
                decompressed = gzip.decompress(file_data)
            except Exception as e:
                raise ValueError(f"Failed to decompress gzip data: {e}")
        elif compression == 'zlib':
            try:
                decompressed = zlib.decompress(file_data)
            except Exception as e:
                raise ValueError(f"Failed to decompress zlib data: {e}")
        else:
            decompressed = file_data
        
        # 嘗試多種讀取模式
        attempts = []
        # 推測 Bedrock 通常為 little-endian，且可能有 8 字節頭
        attempts.append((False, False, 0))  # 標準 Java NBT
        attempts.append((True, True, 8))    # Bedrock（有頭）
        attempts.append((True, False, 0))   # Bedrock（無頭）

        if little_endian is not None or bedrock_header is not None:
            # 如果外部提供了提示，優先使用
            le = little_endian if little_endian is not None else False
            bh = bedrock_header if bedrock_header is not None else False
            off = 8 if bh else 0
            attempts = [(le, bh, off)] + [a for a in attempts if a != (le, bh, off)]

        last_error: Optional[Exception] = None
        for idx, (le, bh, off) in enumerate(attempts):
            try:
                offset = off
                root, _ = cls._read_tag(decompressed, offset, le, read_name=True)
                if not isinstance(root, NbtCompound):
                    raise ValueError("Root tag must be a compound tag")
                # 若根為空，視為可疑，繼續嘗試下一種模式
                if len(root) == 0 and idx < len(attempts) - 1:
                    raise ValueError("Empty root compound, trying next mode")
                return cls(root, compression, le, bh)
            except Exception as e:
                last_error = e
                continue

        # 若所有嘗試失敗
        raise ValueError(f"Failed to read NBT file: {last_error}")
    
    @classmethod
    def _read_tag(cls, data: bytes, offset: int, little_endian: bool, read_name: bool = True) -> Tuple[NbtTag, int]:
        """
        讀取單個 NBT 標籤
        
        Args:
            data: 字節數據
            offset: 當前偏移量
            little_endian: 是否使用 little-endian
            read_name: 是否讀取標籤名稱
            
        Returns:
            (標籤, 新的偏移量) 元組
        """
        if offset >= len(data):
            raise ValueError("Unexpected end of data")
        
        tag_type = data[offset]
        offset += 1
        
        if tag_type == NbtType.END:
            return NbtEnd(), offset
        
        tag_name = ""
        if read_name:
            # 讀取標籤名稱長度
            if offset + 2 > len(data):
                raise ValueError("Unexpected end of data while reading tag name length")
            
            name_length = struct.unpack('<H' if little_endian else '>H', data[offset:offset+2])[0]
            offset += 2
            
            # 讀取標籤名稱
            if offset + name_length > len(data):
                raise ValueError("Unexpected end of data while reading tag name")
            
            tag_name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
        
        # 讀取標籤值
        if tag_type == NbtType.BYTE:
            if offset + 1 > len(data):
                raise ValueError("Unexpected end of data while reading byte value")
            value = struct.unpack('<b' if little_endian else '>b', data[offset:offset+1])[0]
            offset += 1
            tag = NbtByte(value)
            
        elif tag_type == NbtType.SHORT:
            if offset + 2 > len(data):
                raise ValueError("Unexpected end of data while reading short value")
            value = struct.unpack('<h' if little_endian else '>h', data[offset:offset+2])[0]
            offset += 2
            tag = NbtShort(value)
            
        elif tag_type == NbtType.INT:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading int value")
            value = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            tag = NbtInt(value)
            
        elif tag_type == NbtType.LONG:
            if offset + 8 > len(data):
                raise ValueError("Unexpected end of data while reading long value")
            value = struct.unpack('<q' if little_endian else '>q', data[offset:offset+8])[0]
            offset += 8
            tag = NbtLong(value)
            
        elif tag_type == NbtType.FLOAT:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading float value")
            value = struct.unpack('<f' if little_endian else '>f', data[offset:offset+4])[0]
            offset += 4
            tag = NbtFloat(value)
            
        elif tag_type == NbtType.DOUBLE:
            if offset + 8 > len(data):
                raise ValueError("Unexpected end of data while reading double value")
            value = struct.unpack('<d' if little_endian else '>d', data[offset:offset+8])[0]
            offset += 8
            tag = NbtDouble(value)
            
        elif tag_type == NbtType.STRING:
            if offset + 2 > len(data):
                raise ValueError("Unexpected end of data while reading string length")
            str_length = struct.unpack('<H' if little_endian else '>H', data[offset:offset+2])[0]
            offset += 2
            
            if offset + str_length > len(data):
                raise ValueError("Unexpected end of data while reading string value")
            value = data[offset:offset+str_length].decode('utf-8')
            offset += str_length
            tag = NbtString(value)
            
        elif tag_type == NbtType.BYTE_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading byte array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            
            if offset + array_length > len(data):
                raise ValueError("Unexpected end of data while reading byte array values")
            values = list(data[offset:offset+array_length])
            offset += array_length
            tag = NbtByteArray(values)
            
        elif tag_type == NbtType.INT_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading int array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            
            if offset + array_length * 4 > len(data):
                raise ValueError("Unexpected end of data while reading int array values")
            values = list(struct.unpack(f'<{array_length}i' if little_endian else f'>{array_length}i', 
                                      data[offset:offset+array_length*4]))
            offset += array_length * 4
            tag = NbtIntArray(values)
            
        elif tag_type == NbtType.LONG_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading long array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            
            if offset + array_length * 8 > len(data):
                raise ValueError("Unexpected end of data while reading long array values")
            values = list(struct.unpack(f'<{array_length}q' if little_endian else f'>{array_length}q', 
                                      data[offset:offset+array_length*8]))
            offset += array_length * 8
            tag = NbtLongArray(values)
            
        elif tag_type == NbtType.LIST:
            if offset + 5 > len(data):
                raise ValueError("Unexpected end of data while reading list header")
            element_type = data[offset]
            offset += 1
            list_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            elements: List[NbtTag] = []
            for _ in range(list_length):
                elem, offset = cls._read_payload(element_type, data, offset, little_endian)
                elements.append(elem)
            tag = NbtList(elements, element_type)
            
        elif tag_type == NbtType.COMPOUND:
            elements: Dict[str, NbtTag] = {}
            while True:
                if offset >= len(data):
                    raise ValueError("Unexpected end of data while reading compound tag")
                next_tag_type = data[offset]
                offset += 1
                if next_tag_type == NbtType.END:
                    break
                # 名稱
                if offset + 2 > len(data):
                    raise ValueError("Unexpected end of data while reading compound name length")
                name_length = struct.unpack('<H' if little_endian else '>H', data[offset:offset+2])[0]
                offset += 2
                if offset + name_length > len(data):
                    raise ValueError("Unexpected end of data while reading compound name")
                tag_name = data[offset:offset+name_length].decode('utf-8')
                offset += name_length
                # 值（只讀取 payload，不再讀取類型/名稱）
                value_tag, offset = cls._read_payload(next_tag_type, data, offset, little_endian)
                elements[tag_name] = value_tag
            tag = NbtCompound(elements)
            
        else:
            raise ValueError(f"Unknown tag type: {tag_type}")
        
        return tag, offset

    @classmethod
    def _read_payload(cls, tag_type: int, data: bytes, offset: int, little_endian: bool) -> Tuple[NbtTag, int]:
        """在已知 tag 類型的情況下，僅讀取 payload。"""
        if tag_type == NbtType.BYTE:
            if offset + 1 > len(data):
                raise ValueError("Unexpected end of data while reading byte value")
            value = struct.unpack('<b' if little_endian else '>b', data[offset:offset+1])[0]
            return NbtByte(value), offset + 1
        if tag_type == NbtType.SHORT:
            if offset + 2 > len(data):
                raise ValueError("Unexpected end of data while reading short value")
            value = struct.unpack('<h' if little_endian else '>h', data[offset:offset+2])[0]
            return NbtShort(value), offset + 2
        if tag_type == NbtType.INT:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading int value")
            value = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            return NbtInt(value), offset + 4
        if tag_type == NbtType.LONG:
            if offset + 8 > len(data):
                raise ValueError("Unexpected end of data while reading long value")
            value = struct.unpack('<q' if little_endian else '>q', data[offset:offset+8])[0]
            return NbtLong(value), offset + 8
        if tag_type == NbtType.FLOAT:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading float value")
            value = struct.unpack('<f' if little_endian else '>f', data[offset:offset+4])[0]
            return NbtFloat(value), offset + 4
        if tag_type == NbtType.DOUBLE:
            if offset + 8 > len(data):
                raise ValueError("Unexpected end of data while reading double value")
            value = struct.unpack('<d' if little_endian else '>d', data[offset:offset+8])[0]
            return NbtDouble(value), offset + 8
        if tag_type == NbtType.STRING:
            if offset + 2 > len(data):
                raise ValueError("Unexpected end of data while reading string length")
            str_length = struct.unpack('<H' if little_endian else '>H', data[offset:offset+2])[0]
            offset += 2
            if offset + str_length > len(data):
                raise ValueError("Unexpected end of data while reading string value")
            value = data[offset:offset+str_length].decode('utf-8')
            return NbtString(value), offset + str_length
        if tag_type == NbtType.BYTE_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading byte array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            if offset + array_length > len(data):
                raise ValueError("Unexpected end of data while reading byte array values")
            values = list(data[offset:offset+array_length])
            return NbtByteArray(values), offset + array_length
        if tag_type == NbtType.INT_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading int array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            if offset + array_length * 4 > len(data):
                raise ValueError("Unexpected end of data while reading int array values")
            values = list(struct.unpack(f'<{array_length}i' if little_endian else f'>{array_length}i', data[offset:offset+array_length*4]))
            return NbtIntArray(values), offset + array_length * 4
        if tag_type == NbtType.LONG_ARRAY:
            if offset + 4 > len(data):
                raise ValueError("Unexpected end of data while reading long array length")
            array_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            if offset + array_length * 8 > len(data):
                raise ValueError("Unexpected end of data while reading long array values")
            values = list(struct.unpack(f'<{array_length}q' if little_endian else f'>{array_length}q', data[offset:offset+array_length*8]))
            return NbtLongArray(values), offset + array_length * 8
        if tag_type == NbtType.LIST:
            # 嵌套列表：讀 header + N 個 payload
            if offset + 5 > len(data):
                raise ValueError("Unexpected end of data while reading list header")
            element_type = data[offset]
            offset += 1
            list_length = struct.unpack('<i' if little_endian else '>i', data[offset:offset+4])[0]
            offset += 4
            elements: List[NbtTag] = []
            for _ in range(list_length):
                elem, offset = cls._read_payload(element_type, data, offset, little_endian)
                elements.append(elem)
            return NbtList(elements, element_type), offset
        if tag_type == NbtType.COMPOUND:
            elements: Dict[str, NbtTag] = {}
            while True:
                if offset >= len(data):
                    raise ValueError("Unexpected end of data while reading compound payload")
                next_tag_type = data[offset]
                offset += 1
                if next_tag_type == NbtType.END:
                    break
                if offset + 2 > len(data):
                    raise ValueError("Unexpected end of data while reading compound payload name length")
                name_length = struct.unpack('<H' if little_endian else '>H', data[offset:offset+2])[0]
                offset += 2
                if offset + name_length > len(data):
                    raise ValueError("Unexpected end of data while reading compound payload name")
                key = data[offset:offset+name_length].decode('utf-8')
                offset += name_length
                val, offset = cls._read_payload(next_tag_type, data, offset, little_endian)
                elements[key] = val
            return NbtCompound(elements), offset
        raise ValueError(f"Unknown tag type in payload: {tag_type}")
    
    def write(self) -> bytes:
        """
        將 NBT 文件寫入字節序列
        
        Returns:
            字節序列
        """
        # 寫入 Bedrock 頭部
        data = b''
        if self.bedrock_header:
            data += struct.pack('<Q', 0)  # 8 字節的零值
        
        # 寫入根標籤
        data += self._write_tag(self.root)
        
        # 壓縮
        if self.compression == 'gzip':
            return gzip.compress(data)
        elif self.compression == 'zlib':
            return zlib.compress(data)
        else:
            return data
    
    def _write_tag(self, tag: NbtTag, name: str = "") -> bytes:
        """
        將標籤寫入字節序列
        
        Args:
            tag: 要寫入的標籤
            name: 標籤名稱（對於非根標籤）
            
        Returns:
            字節序列
        """
        data = b''
        
        # 寫入標籤類型
        data += struct.pack('<b' if self.little_endian else '>b', tag.type_id)
        
        # 寫入標籤名稱（根標籤允許空名，長度仍需寫入）
        name_bytes = name.encode('utf-8')
        data += struct.pack('<H' if self.little_endian else '>H', len(name_bytes))
        if name_bytes:
            data += name_bytes
        
        # 寫入標籤值
        data += tag.to_bytes(self.little_endian)
        
        return data
    
    def to_json(self) -> Dict[str, Any]:
        """
        將 NBT 文件轉換為 JSON 格式
        
        Returns:
            JSON 字典
        """
        return {
            'root': self.root.to_json(),
            'compression': self.compression,
            'little_endian': self.little_endian,
            'bedrock_header': self.bedrock_header
        }
    
    def __str__(self) -> str:
        return f"NbtFile(compression={self.compression}, little_endian={self.little_endian}, bedrock_header={self.bedrock_header})"
    
    def __repr__(self) -> str:
        return self.__str__()


def read_nbt_file(file_path: str, **kwargs) -> NbtFile:
    """
    從文件路徑讀取 NBT 文件
    
    Args:
        file_path: 文件路徑
        **kwargs: 傳遞給 NbtFile.read 的參數
        
    Returns:
        NbtFile 實例
    """
    with open(file_path, 'rb') as f:
        return NbtFile.read(f, **kwargs)


def write_nbt_file(file_path: str, nbt_file: NbtFile) -> None:
    """
    將 NBT 文件寫入文件
    
    Args:
        file_path: 文件路徑
        nbt_file: 要寫入的 NBT 文件
    """
    with open(file_path, 'wb') as f:
        f.write(nbt_file.write())


def detect_file_format(file_path: str) -> Dict[str, Any]:
    """
    檢測 NBT 文件格式
    
    Args:
        file_path: 文件路徑
        
    Returns:
        包含格式信息的字典
    """
    with open(file_path, 'rb') as f:
        header = f.read(16)
    
    info = {
        'compression': 'none',
        'little_endian': False,
        'bedrock_header': False,
        'file_size': len(header)
    }
    
    # 檢測壓縮類型
    if header.startswith(b'\x1f\x8b'):
        info['compression'] = 'gzip'
    elif header.startswith(b'\x78\x9c') or header.startswith(b'\x78\xda'):
        info['compression'] = 'zlib'
    
    # 檢測 Bedrock 頭部
    if len(header) >= 8 and header[:8] == b'\x08\x00\x00\x00\x00\x00\x00\x00':
        info['bedrock_header'] = True
        info['little_endian'] = True
    
    return info
