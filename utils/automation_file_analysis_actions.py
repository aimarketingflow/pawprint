#!/usr/bin/env python3
"""
File Analysis Actions for Pawprinting PyQt6 V2 Automation

Provides actions for analyzing file content, checking patterns, and extracting data
from files that can be used in automation tasks.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import re
import hashlib
import json
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path

from utils.automation_action_base import Action, ActionResult, ActionContext

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.file_analysis")

class FileHashAction(Action):
    """Action to calculate file hash"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file hash action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Calculate File Hash")
        self.description = self.config.get("description", "Calculates hash of a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file hash action"""
        file_path = self.config.get("file_path")
        algorithm = self.config.get("algorithm", "md5").lower()
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        try:
            context.logger.info(f"Calculating {algorithm} hash for {file_path}")
            
            # Select hash algorithm
            if algorithm == "md5":
                hash_obj = hashlib.md5()
            elif algorithm == "sha1":
                hash_obj = hashlib.sha1()
            elif algorithm == "sha256":
                hash_obj = hashlib.sha256()
            else:
                return ActionResult.failure(f"Unsupported hash algorithm: {algorithm}")
            
            # Calculate hash
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            
            file_hash = hash_obj.hexdigest()
            context.logger.info(f"Hash: {file_hash}")
            
            return ActionResult.success(
                f"File hash calculated successfully",
                {
                    "file_path": file_path,
                    "algorithm": algorithm,
                    "hash": file_hash
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error calculating hash for {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to calculate hash for {file_path}")

class FilePatternMatchAction(Action):
    """Action to check if file content matches a pattern"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file pattern match action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "File Pattern Match")
        self.description = self.config.get("description", "Checks if file content matches a regex pattern")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        if "pattern" not in self.config:
            return False, "Pattern is required"
        
        # Try to compile the regex
        try:
            re.compile(self.config.get("pattern"))
        except re.error:
            return False, "Invalid regex pattern"
            
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file pattern match action"""
        file_path = self.config.get("file_path")
        pattern = self.config.get("pattern")
        extract_matches = self.config.get("extract_matches", False)
        case_insensitive = self.config.get("case_insensitive", False)
        max_matches = self.config.get("max_matches", 100)
        encoding = self.config.get("encoding", "utf-8")
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        try:
            context.logger.info(f"Checking file {file_path} for pattern: {pattern}")
            
            # Compile pattern with flags
            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)
            
            # Read file content
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            
            # Find matches
            matches = list(regex.finditer(content))
            has_match = bool(matches)
            
            if has_match:
                context.logger.info(f"Found {len(matches)} matches")
                result_data = {
                    "file_path": file_path,
                    "pattern": pattern,
                    "has_match": True,
                    "match_count": len(matches)
                }
                
                # Extract matches if requested
                if extract_matches:
                    extracted = []
                    for i, match in enumerate(matches[:max_matches]):
                        extracted.append({
                            "index": i,
                            "text": match.group(0),
                            "groups": match.groups(),
                            "start": match.start(),
                            "end": match.end()
                        })
                    result_data["matches"] = extracted
                
                return ActionResult.success(
                    f"Pattern matched {len(matches)} times",
                    result_data
                )
            else:
                context.logger.info("No matches found")
                return ActionResult.success(
                    "No matches found",
                    {
                        "file_path": file_path,
                        "pattern": pattern,
                        "has_match": False,
                        "match_count": 0
                    }
                )
            
        except UnicodeDecodeError as e:
            context.logger.error(f"Error decoding file {file_path}: {str(e)}")
            return ActionResult.failure(
                f"Failed to decode file with encoding {encoding}",
                {"file_path": file_path, "encoding_error": str(e)}
            )
        except Exception as e:
            context.logger.exception(f"Error searching pattern in {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to search pattern in {file_path}")

class FileJsonExtractAction(Action):
    """Action to extract data from JSON files"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize JSON extraction action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Extract JSON Data")
        self.description = self.config.get("description", "Extracts data from JSON files")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the JSON extraction action"""
        file_path = self.config.get("file_path")
        json_path = self.config.get("json_path", None)  # Optional path to extract
        encoding = self.config.get("encoding", "utf-8")
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        try:
            context.logger.info(f"Extracting JSON data from {file_path}")
            
            # Load JSON data
            with open(file_path, 'r', encoding=encoding) as f:
                json_data = json.load(f)
            
            # Extract specific path if provided
            if json_path:
                context.logger.info(f"Extracting path: {json_path}")
                
                # Split path components
                components = json_path.split('.')
                current = json_data
                
                # Navigate through path
                for component in components:
                    # Handle array indexing
                    if '[' in component and component.endswith(']'):
                        base, index_str = component.split('[', 1)
                        index = int(index_str[:-1])
                        current = current.get(base, [])[index]
                    else:
                        current = current.get(component, {})
                
                extracted_data = current
                
                return ActionResult.success(
                    f"JSON data extracted successfully",
                    {
                        "file_path": file_path,
                        "json_path": json_path,
                        "data": extracted_data
                    }
                )
            else:
                # Return full JSON
                return ActionResult.success(
                    f"JSON data loaded successfully",
                    {
                        "file_path": file_path,
                        "data": json_data
                    }
                )
            
        except json.JSONDecodeError as e:
            context.logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
            return ActionResult.failure(
                f"Failed to parse JSON file",
                {"file_path": file_path, "json_error": str(e)}
            )
        except Exception as e:
            context.logger.exception(f"Error extracting JSON from {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to extract JSON from {file_path}")

class FileLineCountAction(Action):
    """Action to count lines in a file"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize line count action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Count File Lines")
        self.description = self.config.get("description", "Counts lines in a file")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "file_path" not in self.config:
            return False, "File path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the line count action"""
        file_path = self.config.get("file_path")
        encoding = self.config.get("encoding", "utf-8")
        non_empty_only = self.config.get("non_empty_only", False)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return ActionResult.failure(f"File does not exist: {file_path}")
        
        # Check if it's a file
        if not os.path.isfile(file_path):
            return ActionResult.failure(f"Path is not a file: {file_path}")
        
        try:
            context.logger.info(f"Counting lines in {file_path}")
            
            # Count lines
            line_count = 0
            non_empty_count = 0
            
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                for line in f:
                    line_count += 1
                    if line.strip():
                        non_empty_count += 1
            
            if non_empty_only:
                context.logger.info(f"File has {non_empty_count} non-empty lines")
                count = non_empty_count
            else:
                context.logger.info(f"File has {line_count} lines")
                count = line_count
            
            return ActionResult.success(
                f"Line count completed successfully",
                {
                    "file_path": file_path,
                    "line_count": line_count,
                    "non_empty_count": non_empty_count,
                    "count": count
                }
            )
            
        except UnicodeDecodeError as e:
            context.logger.error(f"Error decoding file {file_path}: {str(e)}")
            return ActionResult.failure(
                f"Failed to decode file with encoding {encoding}",
                {"file_path": file_path, "encoding_error": str(e)}
            )
        except Exception as e:
            context.logger.exception(f"Error counting lines in {file_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to count lines in {file_path}")
