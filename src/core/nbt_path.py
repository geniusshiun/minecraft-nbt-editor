"""
NBT 路徑系統
用於定位和操作 NBT 數據結構中的特定位置
"""

from typing import List, Union, Optional, Any


class NbtPath:
    """NBT 路徑類，用於表示 NBT 數據結構中的路徑"""
    
    def __init__(self, path: Union[str, List[Union[str, int]]] = None):
        """
        初始化 NBT 路徑
        
        Args:
            path: 路徑字符串或路徑列表
                字符串格式: "Data.Player.GameType" 或 "Data[0].Name"
                列表格式: ["Data", "Player", "GameType"] 或 ["Data", 0, "Name"]
        """
        if path is None:
            self._arr = []
        elif isinstance(path, str):
            self._arr = self._parse_path_string(path)
        elif isinstance(path, list):
            self._arr = path
        else:
            raise ValueError("Path must be a string or list")
    
    @property
    def arr(self) -> List[Union[str, int]]:
        """返回路徑數組"""
        return self._arr.copy()
    
    def _parse_path_string(self, path_str: str) -> List[Union[str, int]]:
        """解析路徑字符串為路徑數組"""
        if not path_str:
            return []
        
        result = []
        current = ""
        i = 0
        
        while i < len(path_str):
            char = path_str[i]
            
            if char == '.':
                if current:
                    result.append(current)
                    current = ""
            elif char == '[':
                if current:
                    result.append(current)
                    current = ""
                
                # 尋找對應的 ']'
                j = i + 1
                while j < len(path_str) and path_str[j] != ']':
                    j += 1
                
                if j >= len(path_str):
                    raise ValueError(f"Unclosed bracket at position {i}")
                
                # 解析索引
                index_str = path_str[i+1:j]
                try:
                    index = int(index_str)
                    result.append(index)
                except ValueError:
                    raise ValueError(f"Invalid index '{index_str}' at position {i+1}")
                
                i = j
            elif char == ']':
                # 跳過，已經在 '[' 處理中處理了
                pass
            else:
                current += char
            
            i += 1
        
        if current:
            result.append(current)
        
        return result
    
    def pop(self, count: int = 1) -> 'NbtPath':
        """
        返回移除最後 count 個元素的路徑
        
        Args:
            count: 要移除的元素數量
            
        Returns:
            新的 NbtPath 實例
        """
        if count == 0:
            return NbtPath(self._arr)
        return NbtPath(self._arr[:-count])
    
    def shift(self, count: int = 1) -> 'NbtPath':
        """
        返回移除前 count 個元素的路徑
        
        Args:
            count: 要移除的元素數量
            
        Returns:
            新的 NbtPath 實例
        """
        return NbtPath(self._arr[count:])
    
    def push(self, *elements: Union[str, int]) -> 'NbtPath':
        """
        在路徑末尾添加元素
        
        Args:
            *elements: 要添加的元素
            
        Returns:
            新的 NbtPath 實例
        """
        return NbtPath(self._arr + list(elements))
    
    def head(self) -> Optional[Union[str, int]]:
        """返回路徑的第一個元素"""
        return self._arr[0] if self._arr else None
    
    def last(self) -> Optional[Union[str, int]]:
        """返回路徑的最後一個元素"""
        return self._arr[-1] if self._arr else None
    
    def length(self) -> int:
        """返回路徑長度"""
        return len(self._arr)
    
    def starts_with(self, other: 'NbtPath') -> bool:
        """
        檢查當前路徑是否以指定路徑開頭
        
        Args:
            other: 要檢查的前綴路徑
            
        Returns:
            如果當前路徑以指定路徑開頭則返回 True
        """
        if len(other._arr) > len(self._arr):
            return False
        return all(self._arr[i] == other._arr[i] for i in range(len(other._arr)))
    
    def sub_paths(self) -> List['NbtPath']:
        """
        返回所有子路徑
        
        Returns:
            包含所有子路徑的列表，從空路徑到完整路徑
        """
        result = []
        for i in range(len(self._arr) + 1):
            result.append(self.pop(len(self._arr) - i))
        return result
    
    def equals(self, other: 'NbtPath') -> bool:
        """
        檢查兩個路徑是否相等
        
        Args:
            other: 要比較的路徑
            
        Returns:
            如果兩個路徑相等則返回 True
        """
        if not isinstance(other, NbtPath):
            return False
        return len(other._arr) == len(self._arr) and all(other._arr[i] == self._arr[i] for i in range(len(self._arr)))
    
    def __eq__(self, other: Any) -> bool:
        return self.equals(other)
    
    def __hash__(self) -> int:
        return hash(tuple(self._arr))
    
    def __str__(self) -> str:
        """將路徑轉換為字符串表示"""
        if not self._arr:
            return ""
        
        result = ""
        for element in self._arr:
            if isinstance(element, str):
                if result:
                    result += "."
                result += element
            else:  # int
                result += f"[{element}]"
        
        return result
    
    def __repr__(self) -> str:
        return f"NbtPath({self._arr})"
    
    def __len__(self) -> int:
        return len(self._arr)
    
    def __getitem__(self, index: int) -> Union[str, int]:
        return self._arr[index]
    
    def __iter__(self):
        return iter(self._arr)
    
    def is_empty(self) -> bool:
        """檢查路徑是否為空"""
        return len(self._arr) == 0
    
    def is_root(self) -> bool:
        """檢查路徑是否為根路徑（空路徑）"""
        return self.is_empty()
    
    def parent(self) -> 'NbtPath':
        """返回父路徑"""
        if self.is_empty():
            return NbtPath()
        return self.pop(1)
    
    def child(self, element: Union[str, int]) -> 'NbtPath':
        """返回子路徑"""
        return self.push(element)
    
    def common_prefix(self, other: 'NbtPath') -> 'NbtPath':
        """
        返回兩個路徑的公共前綴
        
        Args:
            other: 另一個路徑
            
        Returns:
            公共前綴路徑
        """
        common = []
        for i in range(min(len(self._arr), len(other._arr))):
            if self._arr[i] == other._arr[i]:
                common.append(self._arr[i])
            else:
                break
        return NbtPath(common)
    
    def relative_to(self, base: 'NbtPath') -> 'NbtPath':
        """
        返回相對於基路徑的路徑
        
        Args:
            base: 基路徑
            
        Returns:
            相對路徑
            
        Raises:
            ValueError: 如果當前路徑不是基路徑的子路徑
        """
        if not self.starts_with(base):
            raise ValueError(f"Path {self} is not a subpath of {base}")
        return NbtPath(self._arr[len(base._arr):])
    
    def validate(self) -> bool:
        """
        驗證路徑的有效性
        
        Returns:
            如果路徑有效則返回 True
        """
        for element in self._arr:
            if not (isinstance(element, str) or isinstance(element, int)):
                return False
            if isinstance(element, str) and not element:
                return False
        return True
