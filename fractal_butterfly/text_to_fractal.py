#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text to Fractal Converter for Pawprinting PyQt6 Application

This module handles the conversion of text input into fractal parameters
that generate a unique base fractal pattern.
"""

import hashlib
import numpy as np
import math
import logging
from typing import Dict, Any, Tuple, List, Optional
import json
import os
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

class TextToFractalConverter:
    """
    Converts text input into fractal parameters and generates base fractal patterns
    """
    
    def __init__(self):
        """Initialize converter with default settings"""
        self.max_text_length = 2000
        self.min_text_length = 1
        
        # Define parameter ranges
        self.param_ranges = {
            "fractal_dimension": (1.0, 2.0),
            "wing_ratio": (1.0, 4.0),
            "symmetry": (0.0, 1.0),
            "density": (0.0, 1.0),
            "iterations": (100, 2000),
            "resolution": [(200, 1200), (200, 1200)],
            "color_scheme": ["rainbow", "bluescale", "heatmap", "grayscale", "cosmic"]
        }
        
        # Define base fractal types
        self.fractal_types = ["mandelbrot", "julia", "burning_ship", "tricorn", "multibrot"]
        
        # Configuration save directory
        self.config_dir = os.path.expanduser("~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/configs")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
    
    def text_to_parameters(self, text: str, num_sampling_points: int = 5, sequence_length: int = 3) -> Dict[str, Any]:
        """
        Convert text input to fractal parameters
        
        Args:
            text: Input text (1-2000 characters)
            num_sampling_points: Number of sampling points for Pash generation (default: 5)
            sequence_length: Number of characters to extract at each sampling point (default: 3)
            
        Returns:
            Dictionary of fractal parameters
        """
        if not text or len(text) < self.min_text_length:
            raise ValueError(f"Text must be at least {self.min_text_length} character")
            
        if len(text) > self.max_text_length:
            raise ValueError(f"Text exceeds maximum length of {self.max_text_length} characters")
        
        logger.info(f"Converting text of length {len(text)} to fractal parameters")
        
        # Create a primary hash of the text
        text_hash = hashlib.sha256(text.encode()).digest()
        
        # Create a secondary hash with a different algorithm for more entropy
        secondary_hash = hashlib.sha512(text.encode()).digest()
        
        # Text analysis metrics
        char_counts = {}
        word_count = len(text.split())
        line_count = len(text.splitlines())
        
        # Count character types
        alpha_count = sum(c.isalpha() for c in text)
        digit_count = sum(c.isdigit() for c in text)
        special_count = len(text) - alpha_count - digit_count
        
        # Calculate entropy of text
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0.0
        for count in char_counts.values():
            freq = count / len(text)
            entropy -= freq * math.log2(freq) if freq > 0 else 0
        
        # Normalize entropy (0-8 bits typical range for text)
        norm_entropy = min(entropy / 8.0, 1.0)
        
        # Generate parameters from text properties
        
        # Convert first 4 bytes of hash to a normalized float 0-1
        hash_float = int.from_bytes(text_hash[:4], byteorder='big') / (2**32 - 1)
        
        # Fractal dimension influenced by character distribution (entropy)
        fractal_dim_range = self.param_ranges["fractal_dimension"]
        fractal_dimension = fractal_dim_range[0] + norm_entropy * (fractal_dim_range[1] - fractal_dim_range[0])
        
        # Wing ratio influenced by word count and hash
        wing_ratio_range = self.param_ranges["wing_ratio"]
        wing_ratio_factor = min(word_count / 100, 1.0)  # Normalize to 0-1
        wing_ratio_hash = int.from_bytes(text_hash[4:8], byteorder='big') / (2**32 - 1)
        wing_ratio = wing_ratio_range[0] + (wing_ratio_factor * 0.7 + wing_ratio_hash * 0.3) * (wing_ratio_range[1] - wing_ratio_range[0])
        
        # Symmetry based on text structure and secondary hash
        sym_hash = int.from_bytes(secondary_hash[:4], byteorder='big') / (2**32 - 1)
        symmetry_factor = min(line_count / 50, 1.0)  # Normalize to 0-1
        symmetry = symmetry_factor * 0.6 + sym_hash * 0.4
        
        # Density based on special characters ratio and hash
        density_hash = int.from_bytes(secondary_hash[4:8], byteorder='big') / (2**32 - 1)
        special_ratio = special_count / max(len(text), 1)
        density = special_ratio * 0.5 + density_hash * 0.5
        
        # Iterations based on text length
        iter_range = self.param_ranges["iterations"]
        length_factor = min(len(text) / self.max_text_length, 1.0)
        iterations = int(iter_range[0] + length_factor * (iter_range[1] - iter_range[0]))
        
        # Resolution based on text complexity
        width_range = self.param_ranges["resolution"][0]
        height_range = self.param_ranges["resolution"][1]
        
        complexity = (len(char_counts) / 256) * 0.7 + norm_entropy * 0.3  # Normalized complexity factor
        
        width = int(width_range[0] + complexity * (width_range[1] - width_range[0]))
        height = int(height_range[0] + complexity * (height_range[1] - height_range[0]))
        
        # Round to nearest 100 for cleaner values
        width = round(width / 100) * 100
        height = round(height / 100) * 100
        
        # Select color scheme based on character distribution
        alpha_ratio = alpha_count / max(len(text), 1)
        digit_ratio = digit_count / max(len(text), 1)
        
        color_idx = int((alpha_ratio * 3 + digit_ratio * 2) * len(self.param_ranges["color_scheme"]))
        color_idx = min(color_idx, len(self.param_ranges["color_scheme"]) - 1)
        color_scheme = self.param_ranges["color_scheme"][color_idx]
        
        # Select base fractal pattern from hash
        fractal_idx = int(hash_float * len(self.fractal_types))
        fractal_idx = min(fractal_idx, len(self.fractal_types) - 1)
        base_fractal_pattern = self.fractal_types[fractal_idx]
        
        # Generate base fractal influence based on text properties
        base_influence = 0.3 + norm_entropy * 0.7  # Higher entropy = more influence
        
        # Generate Pawprint Signature ('Pash')
        pash_string = ""
        if text: # Only generate if text is not empty
            # Use the customizable parameters passed from UI
            pash_segments = []
            min_bytes_needed_for_seeds = num_sampling_points * 2 # Each seed takes 2 bytes

            if len(text_hash) >= min_bytes_needed_for_seeds:
                for i in range(num_sampling_points):
                    start_byte_offset = i * 2
                    current_seed_bytes = text_hash[start_byte_offset : start_byte_offset + 2]
                    index_seed = int.from_bytes(current_seed_bytes, byteorder='big')
                    
                    actual_sampling_index = index_seed % len(text)
                    end_char_index = min(actual_sampling_index + sequence_length, len(text))
                    segment = text[actual_sampling_index : end_char_index]
                    pash_segments.append(segment)
                pash_string = "".join(pash_segments)
            else:
                logger.warning(f"text_hash too short ({len(text_hash)} bytes) to generate all Pash segments. Needs at least {min_bytes_needed_for_seeds} bytes.")
                # Use fallback for short hashes - take what we can get
                bytes_available = len(text_hash) // 2
                for i in range(bytes_available):
                    start_byte_offset = i * 2
                    current_seed_bytes = text_hash[start_byte_offset : start_byte_offset + 2]
                    index_seed = int.from_bytes(current_seed_bytes, byteorder='big')
                    
                    actual_sampling_index = index_seed % len(text)
                    end_char_index = min(actual_sampling_index + sequence_length, len(text))
                    segment = text[actual_sampling_index : end_char_index]
                    pash_segments.append(segment)
                
                pash_string = "".join(pash_segments)
        
        # Create parameter dictionary
        params = {
            "text_input": text,
            "fractal_dimension": round(fractal_dimension, 2),
            "wing_ratio": round(wing_ratio, 2),
            "symmetry": round(symmetry, 2),
            "density": round(density, 2),
            "iterations": iterations,
            "resolution": (width, height),
            "color_scheme": color_scheme,
            "use_base_fractal": True,
            "base_fractal_pattern": base_fractal_pattern,
            "base_fractal_influence": round(base_influence, 2),
            "text_entropy": round(norm_entropy, 3),
            "pawprint_signature": pash_string,
            "pash_settings": {
                "sampling_points": num_sampling_points,
                "sequence_length": sequence_length
            },
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"Generated parameters from text: {params}")
        return params
    
    def save_configuration(self, params: Dict[str, Any], name: str = None) -> str:
        """
        Save fractal configuration to file
        
        Args:
            params: Parameter dictionary
            name: Optional configuration name (defaults to timestamp)
            
        Returns:
            Path to saved configuration file
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"fractal_config_{timestamp}"
        
        # Ensure valid filename
        name = name.replace(" ", "_").replace("/", "_")
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Add metadata
        config = params.copy()
        if "created_at" not in config:
            config["created_at"] = datetime.now().isoformat()
        
        config["name"] = name
        
        # Write to file
        file_path = os.path.join(self.config_dir, f"{name}.json")
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Saved configuration to {file_path}")
        return file_path
    
    def load_configuration(self, file_path: str) -> Dict[str, Any]:
        """
        Load fractal configuration from file
        
        Args:
            file_path: Path to configuration file
            
        Returns:
            Parameter dictionary
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            config = json.load(f)
        
        logger.info(f"Loaded configuration from {file_path}")
        return config
    
    def list_configurations(self) -> List[Dict[str, Any]]:
        """
        List all saved configurations
        
        Returns:
            List of configuration metadata (name, created_at, file_path)
        """
        configs = []
        
        if not os.path.exists(self.config_dir):
            return configs
        
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.config_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        config = json.load(f)
                    
                    # Extract metadata
                    meta = {
                        "name": config.get("name", filename[:-5]),
                        "created_at": config.get("created_at", "Unknown"),
                        "file_path": file_path
                    }
                    configs.append(meta)
                except Exception as e:
                    logger.error(f"Error reading configuration {filename}: {e}")
        
        # Sort by creation date (newest first)
        configs.sort(key=lambda x: x["created_at"], reverse=True)
        return configs
