"""
NBT 標籤類型定義
實現所有 Minecraft NBT 格式支援的標籤類型
"""

import struct
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Tuple
from enum import IntEnum


class NbtType(IntEnum):
    """NBT 標籤類型枚舉"""
    END = 0
    BYTE = 1
    SHORT = 2
    INT = 3
    LONG = 4
    FLOAT = 5
    DOUBLE = 6
    BYTE_ARRAY = 7
    STRING = 8
    LIST = 9
    COMPOUND = 10
    INT_ARRAY = 11
    LONG_ARRAY = 12


class NbtTag(ABC):
    """NBT 標籤基類"""
    
    def __init__(self, value: Any = None):
        self._value = value
    
    @property
    @abstractmethod
    def type_id(self) -> int:
        """返回標籤類型 ID"""
        pass
    
    @property
    def value(self) -> Any:
        """返回標籤值"""
        return self._value
    
    @value.setter
    def value(self, new_value: Any):
        """設置標籤值"""
        self._value = new_value
    
    @abstractmethod
    def to_bytes(self, little_endian: bool = False) -> bytes:
        """將標籤轉換為字節序列"""
        pass
    
    @abstractmethod
    def to_json(self) -> Any:
        """將標籤轉換為 JSON 格式"""
        pass
    
    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value})"
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NbtTag):
            return False
        return self.type_id == other.type_id and self._value == other._value


class NbtEnd(NbtTag):
    """NBT End 標籤"""
    
    def __init__(self):
        super().__init__(None)
    
    @property
    def type_id(self) -> int:
        return NbtType.END
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return b''
    
    def to_json(self) -> None:
        return None


class NbtByte(NbtTag):
    """NBT Byte 標籤"""
    
    def __init__(self, value: int = 0):
        if not isinstance(value, int):
            raise ValueError("Byte value must be an integer")
        if not -128 <= value <= 127:
            raise ValueError("Byte value must be between -128 and 127")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.BYTE
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<b' if little_endian else '>b', self._value)
    
    def to_json(self) -> int:
        return self._value


class NbtShort(NbtTag):
    """NBT Short 標籤"""
    
    def __init__(self, value: int = 0):
        if not isinstance(value, int):
            raise ValueError("Short value must be an integer")
        if not -32768 <= value <= 32767:
            raise ValueError("Short value must be between -32768 and 32767")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.SHORT
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<h' if little_endian else '>h', self._value)
    
    def to_json(self) -> int:
        return self._value


class NbtInt(NbtTag):
    """NBT Int 標籤"""
    
    def __init__(self, value: int = 0):
        if not isinstance(value, int):
            raise ValueError("Int value must be an integer")
        if not -2147483648 <= value <= 2147483647:
            raise ValueError("Int value must be between -2147483648 and 2147483647")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.INT
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<i' if little_endian else '>i', self._value)
    
    def to_json(self) -> int:
        return self._value


class NbtLong(NbtTag):
    """NBT Long 標籤"""
    
    def __init__(self, value: int = 0):
        if not isinstance(value, int):
            raise ValueError("Long value must be an integer")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.LONG
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<q' if little_endian else '>q', self._value)
    
    def to_json(self) -> int:
        return self._value


class NbtFloat(NbtTag):
    """NBT Float 標籤"""
    
    def __init__(self, value: float = 0.0):
        if not isinstance(value, (int, float)):
            raise ValueError("Float value must be a number")
        super().__init__(float(value))
    
    @property
    def type_id(self) -> int:
        return NbtType.FLOAT
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<f' if little_endian else '>f', self._value)
    
    def to_json(self) -> float:
        return self._value


class NbtDouble(NbtTag):
    """NBT Double 標籤"""
    
    def __init__(self, value: float = 0.0):
        if not isinstance(value, (int, float)):
            raise ValueError("Double value must be a number")
        super().__init__(float(value))
    
    @property
    def type_id(self) -> int:
        return NbtType.DOUBLE
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        return struct.pack('<d' if little_endian else '>d', self._value)
    
    def to_json(self) -> float:
        return self._value


class NbtString(NbtTag):
    """NBT String 標籤"""
    
    def __init__(self, value: str = ""):
        if not isinstance(value, str):
            raise ValueError("String value must be a string")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.STRING
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        value_bytes = self._value.encode('utf-8')
        length = len(value_bytes)
        return struct.pack('<H' if little_endian else '>H', length) + value_bytes
    
    def to_json(self) -> str:
        return self._value


class NbtByteArray(NbtTag):
    """NBT Byte Array 標籤"""
    
    def __init__(self, value: List[int] = None):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("Byte array value must be a list")
        for item in value:
            if not isinstance(item, int) or not -128 <= item <= 127:
                raise ValueError("Byte array items must be integers between -128 and 127")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.BYTE_ARRAY
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        length = len(self._value)
        length_bytes = struct.pack('<i' if little_endian else '>i', length)
        data_bytes = struct.pack(f'<{length}b' if little_endian else f'>{length}b', *self._value)
        return length_bytes + data_bytes
    
    def to_json(self) -> List[int]:
        return self._value.copy()


class NbtIntArray(NbtTag):
    """NBT Int Array 標籤"""
    
    def __init__(self, value: List[int] = None):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("Int array value must be a list")
        for item in value:
            if not isinstance(item, int):
                raise ValueError("Int array items must be integers")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.INT_ARRAY
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        length = len(self._value)
        length_bytes = struct.pack('<i' if little_endian else '>i', length)
        data_bytes = struct.pack(f'<{length}i' if little_endian else f'>{length}i', *self._value)
        return length_bytes + data_bytes
    
    def to_json(self) -> List[int]:
        return self._value.copy()


class NbtLongArray(NbtTag):
    """NBT Long Array 標籤"""
    
    def __init__(self, value: List[int] = None):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("Long array value must be a list")
        for item in value:
            if not isinstance(item, int):
                raise ValueError("Long array items must be integers")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.LONG_ARRAY
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        length = len(self._value)
        length_bytes = struct.pack('<i' if little_endian else '>i', length)
        data_bytes = struct.pack(f'<{length}q' if little_endian else f'>{length}q', *self._value)
        return length_bytes + data_bytes
    
    def to_json(self) -> List[int]:
        return self._value.copy()


class NbtList(NbtTag):
    """NBT List 標籤"""
    
    def __init__(self, value: List[NbtTag] = None, element_type: Optional[int] = None):
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError("List value must be a list")
        for item in value:
            if not isinstance(item, NbtTag):
                raise ValueError("List items must be NBT tags")
        super().__init__(value)
        self._element_type = element_type
    
    @property
    def type_id(self) -> int:
        return NbtType.LIST
    
    @property
    def element_type(self) -> Optional[int]:
        """返回列表元素類型，如果列表為空則返回 None"""
        if self._element_type is not None:
            return self._element_type
        if self._value:
            return self._value[0].type_id
        return None
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        element_type = self.element_type
        if element_type is None:
            element_type = NbtType.END
        
        length = len(self._value)
        type_bytes = struct.pack('<b' if little_endian else '>b', element_type)
        length_bytes = struct.pack('<i' if little_endian else '>i', length)
        
        data_bytes = b''
        for item in self._value:
            data_bytes += item.to_bytes(little_endian)
        
        return type_bytes + length_bytes + data_bytes
    
    def to_json(self) -> List[Any]:
        return [item.to_json() for item in self._value]


class NbtCompound(NbtTag):
    """NBT Compound 標籤"""
    
    def __init__(self, value: Dict[str, NbtTag] = None):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError("Compound value must be a dictionary")
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("Compound keys must be strings")
            if not isinstance(item, NbtTag):
                raise ValueError("Compound values must be NBT tags")
        super().__init__(value)
    
    @property
    def type_id(self) -> int:
        return NbtType.COMPOUND
    
    def to_bytes(self, little_endian: bool = False) -> bytes:
        data_bytes = b''
        for key, value in self._value.items():
            # 寫入標籤類型
            data_bytes += struct.pack('<b' if little_endian else '>b', value.type_id)
            # 寫入鍵名
            key_bytes = key.encode('utf-8')
            key_length = len(key_bytes)
            data_bytes += struct.pack('<H' if little_endian else '>H', key_length)
            data_bytes += key_bytes
            # 寫入值
            data_bytes += value.to_bytes(little_endian)
        
        # 寫入結束標籤
        data_bytes += struct.pack('<b' if little_endian else '>b', NbtType.END)
        return data_bytes
    
    def to_json(self) -> Dict[str, Any]:
        return {key: value.to_json() for key, value in self._value.items()}
    
    def get(self, key: str, default: Any = None) -> Optional[NbtTag]:
        """獲取指定鍵的值"""
        return self._value.get(key, default)
    
    def set(self, key: str, value: NbtTag):
        """設置指定鍵的值"""
        if not isinstance(value, NbtTag):
            raise ValueError("Value must be an NBT tag")
        self._value[key] = value
    
    def delete(self, key: str):
        """刪除指定鍵"""
        if key in self._value:
            del self._value[key]
    
    def has(self, key: str) -> bool:
        """檢查是否包含指定鍵"""
        return key in self._value
    
    def keys(self):
        """返回所有鍵"""
        return self._value.keys()
    
    def values(self):
        """返回所有值"""
        return self._value.values()
    
    def items(self):
        """返回所有鍵值對"""
        return self._value.items()
    
    def __getitem__(self, key: str) -> NbtTag:
        return self._value[key]
    
    def __setitem__(self, key: str, value: NbtTag):
        self.set(key, value)
    
    def __delitem__(self, key: str):
        self.delete(key)
    
    def __contains__(self, key: str) -> bool:
        return key in self._value
    
    def __len__(self) -> int:
        return len(self._value)


# 便利函數
def create_tag(tag_type: int, value: Any) -> NbtTag:
    """根據類型創建 NBT 標籤"""
    tag_classes = {
        NbtType.END: NbtEnd,
        NbtType.BYTE: NbtByte,
        NbtType.SHORT: NbtShort,
        NbtType.INT: NbtInt,
        NbtType.LONG: NbtLong,
        NbtType.FLOAT: NbtFloat,
        NbtType.DOUBLE: NbtDouble,
        NbtType.STRING: NbtString,
        NbtType.BYTE_ARRAY: NbtByteArray,
        NbtType.INT_ARRAY: NbtIntArray,
        NbtType.LONG_ARRAY: NbtLongArray,
        NbtType.LIST: NbtList,
        NbtType.COMPOUND: NbtCompound,
    }
    
    if tag_type not in tag_classes:
        raise ValueError(f"Unknown NBT tag type: {tag_type}")
    
    tag_class = tag_classes[tag_type]
    return tag_class(value)
