"""
國際化支援模組
支援中文和英文顯示
"""

import locale
import os
from typing import Dict, Any

# 支援的語言
SUPPORTED_LANGUAGES = ['en', 'zh']

# 語言映射
LANGUAGE_MAPPING = {
    'en': 'en_US.UTF-8',
    'zh': 'zh_TW.UTF-8',
    'zh_CN': 'zh_CN.UTF-8',
    'zh_TW': 'zh_TW.UTF-8',
}

# 翻譯文本
TRANSLATIONS = {
    'en': {
        'app_title': 'Minecraft NBT Editor - Supporting Java and Bedrock editions',
        'reading_file': 'Reading file: {}',
        'file_format': 'File format: {}',
        'file_type': 'File type: {}',
        'compression': 'Compression: {}',
        'byte_order': 'Byte order: {}',
        'bedrock_header': 'Bedrock header: {}',
        'file_content': 'File content:',
        'path_content': 'Content at path {}:',
        'error': '❌ Error: {}',
        'success': '✅ Success!',
        'analyzing_file': 'Analyzing file: {}',
        'file_info': 'File Information',
        'attribute': 'Attribute',
        'value': 'Value',
        'file_path': 'File path',
        'file_size': 'File size',
        'bytes': 'bytes',
        'root_tag_type': 'Root tag type',
        'nbt_compression': 'NBT compression',
        'nbt_byte_order': 'NBT byte order',
        'nbt_bedrock_header': 'NBT Bedrock header',
        'modifying_file': 'Modifying file: {}',
        'path': 'Path',
        'new_value': 'New value',
        'adding_tag': 'Adding tag to file: {}',
        'value_to_add': 'Value to add',
        'removing_tag': 'Removing tag from file: {}',
        'searching_file': 'Searching file: {}',
        'no_results': 'No matching results found',
        'found_results': 'Found {} matching results:',
        'result_path': 'Path',
        'result_type': 'Type',
        'result_value': 'Value',
        'max_depth_reached': '... (max depth reached)',
        'items': 'items',
        'folder_icon': '📁',
        'file_icon': '📄',
        'error_icon': '❌',
        'success_icon': '✅',
        'commands': {
            'add': 'Add new tag to NBT path',
            'enable': 'Enable Minecraft features',
            'info': 'Display NBT file information',
            'remove': 'Remove tag from NBT path',
            'search': 'Search tags in NBT file',
            'set': 'Set value at NBT path',
            'view': 'View NBT file content',
        },
        'options': {
            'format': 'Output format',
            'max_depth': 'Maximum depth',
            'path': 'Only show content at specified path',
            'value': 'New value',
            'type': 'Value type (auto-detect)',
            'tag_type': 'Tag type to search',
            'tag_name': 'Tag name to search',
        },
        'formats': {
            'tree': 'Tree structure',
            'table': 'Table format',
            'json': 'JSON format',
        },
        'enable': {
            'enabling_experiments': '🧪 Enabling all experimental features...',
            'backup_created': '✅ Backup created: {}',
            'feature_enabled': '  ✓ {}: {}',
            'all_enabled': '✅ All experimental features enabled!',
            'restart_hint': '💡 Tip: Restart the world for changes to take effect',
            'specify_option': '❌ Please specify a feature option',
            'available_options': 'Available options:',
            'exp_option': '  --exp    Enable all experimental features',
        },
    },
    'zh': {
        'app_title': 'Minecraft NBT 編輯器 - 支援 Java 和 Bedrock 版本',
        'reading_file': '正在讀取文件: {}',
        'file_format': '文件格式: {}',
        'file_type': '文件類型: {}',
        'compression': '壓縮: {}',
        'byte_order': '字節序: {}',
        'bedrock_header': 'Bedrock 頭部: {}',
        'file_content': '文件內容:',
        'path_content': '路徑 {} 的內容:',
        'error': '❌ 錯誤: {}',
        'success': '✅ 成功！',
        'analyzing_file': '正在分析文件: {}',
        'file_info': '文件信息',
        'attribute': '屬性',
        'value': '值',
        'file_path': '文件路徑',
        'file_size': '文件大小',
        'bytes': 'bytes',
        'root_tag_type': '根標籤類型',
        'nbt_compression': 'NBT 壓縮',
        'nbt_byte_order': 'NBT 字節序',
        'nbt_bedrock_header': 'NBT Bedrock 頭部',
        'modifying_file': '正在修改文件: {}',
        'path': '路徑',
        'new_value': '新值',
        'adding_tag': '正在添加標籤到文件: {}',
        'value_to_add': '要添加的值',
        'removing_tag': '正在從文件刪除標籤: {}',
        'searching_file': '正在搜索文件: {}',
        'no_results': '未找到匹配的結果',
        'found_results': '找到 {} 個匹配結果:',
        'result_path': '路徑',
        'result_type': '類型',
        'result_value': '值',
        'max_depth_reached': '... (已達最大深度)',
        'items': '項目',
        'folder_icon': '📁',
        'file_icon': '📄',
        'error_icon': '❌',
        'success_icon': '✅',
        'commands': {
            'add': '在 NBT 路徑添加新標籤',
            'enable': '啟用 Minecraft 功能',
            'info': '顯示 NBT 文件信息',
            'remove': '從 NBT 路徑刪除標籤',
            'search': '搜索 NBT 文件中的標籤',
            'set': '設置 NBT 路徑的值',
            'view': '查看 NBT 文件內容',
        },
        'options': {
            'format': '輸出格式',
            'max_depth': '最大深度',
            'path': '只顯示指定路徑的內容',
            'value': '新值',
            'type': '值類型 (自動檢測)',
            'tag_type': '搜索標籤類型',
            'tag_name': '搜索標籤名稱',
        },
        'formats': {
            'tree': '樹狀結構',
            'table': '表格格式',
            'json': 'JSON 格式',
        },
        'enable': {
            'enabling_experiments': '🧪 正在啟用所有實驗性功能...',
            'backup_created': '✅ 已創建備份: {}',
            'feature_enabled': '  ✓ {}: {}',
            'all_enabled': '✅ 所有實驗性功能已啟用！',
            'restart_hint': '💡 提示: 重新啟動世界以使更改生效',
            'specify_option': '❌ 請指定要啟用的功能選項',
            'available_options': '可用選項:',
            'exp_option': '  --exp    啟用所有實驗性功能',
        },
    }
}


def get_system_language() -> str:
    """檢測系統語言"""
    try:
        # 嘗試從環境變數獲取語言
        lang = os.environ.get('LANG', '')
        if lang:
            lang = lang.split('_')[0]
            if lang in SUPPORTED_LANGUAGES:
                return lang
        
        # 嘗試從 locale 獲取語言
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            lang = system_locale.split('_')[0]
            if lang in SUPPORTED_LANGUAGES:
                return lang
        
        # 默認使用英文
        return 'en'
    except:
        return 'en'


def get_text(key: str, *args, language: str = None) -> str:
    """獲取翻譯文本"""
    if language is None:
        language = get_system_language()
    
    # 如果請求的語言不支持，使用英文
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'
    
    # 處理嵌套鍵值 (如 'commands.add')
    keys = key.split('.')
    value = TRANSLATIONS[language]
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # 如果找不到翻譯，返回英文版本
            value = TRANSLATIONS['en']
            for k2 in keys:
                if isinstance(value, dict) and k2 in value:
                    value = value[k2]
                else:
                    return key  # 如果都找不到，返回鍵名
    
    # 格式化文本
    if args:
        try:
            return value.format(*args)
        except:
            return str(value)
    
    return str(value)


def get_language_info() -> Dict[str, Any]:
    """獲取語言信息"""
    current_lang = get_system_language()
    return {
        'current': current_lang,
        'supported': SUPPORTED_LANGUAGES,
        'system_locale': locale.getdefaultlocale(),
        'env_lang': os.environ.get('LANG'),
        'env_language': os.environ.get('LANGUAGE'),
        'env_lc_all': os.environ.get('LC_ALL'),
    }
