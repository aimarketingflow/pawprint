#!/usr/bin/env python3
"""
File Content Actions for Pawprinting PyQt6 V2 Automation

Provides actions for reading, writing, and manipulating file contents
that can be used in automation tasks.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import re
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path

from utils.automation_action_base import Action, ActionResult, ActionContext

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.file_content")

class FileReadAction(Action):
    """Action to read content from a file"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file read action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Read File Content")
        self.description = self.config.get("description", "Reads content from a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file read action"""
        file_path = self.config.get("file_path")
        encoding = self.config.get("encoding", "utf-8")
        max_size = self.config.get("max_size", 10 * 1024 * 1024)  # 10MB default limit
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            return ActionResult.failure(
                f"File size ({file_size} bytes) exceeds maximum allowed size ({max_size} bytes)"
            )
        
        try:
            context.logger.info(f"Reading content from {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            
            context.logger.info(f"Read {len(content)} characters from {file_path}")
            
            return ActionResult.success(
                f"File content read successfully",
                {
                    "file_path": file_path,
                    "content": content,
                    "size": len(content)
                }
            )
            
        except UnicodeDecodeError as e:
            context.logger.error(f"Error decoding file {file_path}: {str(e)}")
            return ActionResult.failure(
                f"Failed to decode file with encoding {encoding}",
                {"file_path": file_path, "encoding_error": str(e)}
            )
        except Exception as e:
            context.logger.exception(f"Error reading content from {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to read content from {file_path}")

class FileWriteAction(Action):
    """Action to write content to a file"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file write action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Write File Content")
        self.description = self.config.get("description", "Writes content to a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        if "content" not in self.config:
            return False, "Content is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file write action"""
        file_path = self.config.get("file_path")
        content = self.config.get("content")
        encoding = self.config.get("encoding", "utf-8")
        append = self.config.get("append", False)
        create_dirs = self.config.get("create_dirs", True)
        
        try:
            # Create parent directories if needed
            if create_dirs:
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            context.logger.info(f"{'Appending to' if append else 'Writing'} {file_path}")
            
            # Write content to file
            mode = 'a' if append else 'w'
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            
            context.logger.info(f"Wrote {len(content)} characters to {file_path}")
            
            return ActionResult.success(
                f"Content {'appended to' if append else 'written to'} file successfully",
                {
                    "file_path": file_path,
                    "size": len(content),
                    "append": append
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error writing to {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to write to {file_path}")

class FileAppendAction(Action):
    """Action to append content to a file"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file append action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Append to File")
        self.description = self.config.get("description", "Appends content to a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        if "content" not in self.config:
            return False, "Content is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file append action"""
        # This is just a specialized case of FileWriteAction with append=True
        # We could reuse that logic, but keeping separate for clarity
        
        file_path = self.config.get("file_path")
        content = self.config.get("content")
        encoding = self.config.get("encoding", "utf-8")
        create_dirs = self.config.get("create_dirs", True)
        
        try:
            # Create parent directories if needed
            if create_dirs:
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            context.logger.info(f"Appending to {file_path}")
            
            # Append content to file
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            
            context.logger.info(f"Appended {len(content)} characters to {file_path}")
            
            return ActionResult.success(
                f"Content appended to file successfully",
                {
                    "file_path": file_path,
                    "size": len(content)
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error appending to {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to append to {file_path}")

class FileReplaceTextAction(Action):
    """Action to find and replace text in a file"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file replace text action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Find and Replace in File")
        self.description = self.config.get("description", "Finds and replaces text in a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        if "find" not in self.config:
            return False, "Find text is required"
        if "replace" not in self.config:
            return False, "Replace text is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file replace text action"""
        file_path = self.config.get("file_path")
        find_text = self.config.get("find")
        replace_text = self.config.get("replace")
        encoding = self.config.get("encoding", "utf-8")
        regex = self.config.get("regex", False)
        case_sensitive = self.config.get("case_sensitive", True)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        try:
            context.logger.info(f"Finding and replacing text in {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            
            # Perform replacement
            if regex:
                # Use regex replace
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(find_text, flags)
                new_content, count = re.subn(pattern, replace_text, content)
            else:
                # Use string replace
                if not case_sensitive:
                    def replace_case_insensitive(s, old, new):
                        import re
                        pattern = re.compile(re.escape(old), re.IGNORECASE)
                        return pattern.sub(new, s)
                    
                    new_content, count = re.subn(
                        re.compile(re.escape(find_text), re.IGNORECASE),
                        replace_text,
                        content
                    )
                else:
                    new_content = content.replace(find_text, replace_text)
                    count = content.count(find_text)
            
            # Write modified content back to file
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(new_content)
            
            context.logger.info(f"Made {count} replacements in {file_path}")
            
            return ActionResult.success(
                f"Text replaced successfully ({count} occurrences)",
                {
                    "file_path": file_path,
                    "replacements": count,
                    "original_size": len(content),
                    "new_size": len(new_content)
                }
            )
            
        except UnicodeDecodeError as e:
            context.logger.error(f"Error decoding file {file_path}: {str(e)}")
            return ActionResult.failure(
                f"Failed to decode file with encoding {encoding}",
                {"file_path": file_path, "encoding_error": str(e)}
            )
        except Exception as e:
            context.logger.exception(f"Error replacing text in {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to replace text in {file_path}")
