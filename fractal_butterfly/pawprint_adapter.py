#!/usr/bin/env python3
"""
Pawprint Adapter Module

Adapts pawprint data for use with fractal butterfly generation.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import json
import logging
import numpy as np
from typing import Dict, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.adapter")

class PawprintAdapter:
    """
    Class for adapting pawprint data for fractal butterfly generation
    """
    
    def __init__(self):
        """Initialize the pawprint adapter"""
        pass
    
    def extract_parameters_from_pawprint(self, pawprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract parameters from pawprint data for fractal generation
        
        Args:
            pawprint_data: Dictionary containing pawprint data
            
        Returns:
            Dictionary of parameters for fractal generation
        """
        logger.info("Extracting parameters from pawprint data")
        
        # Default parameters
        params = {
            "fractal_dimension": 1.5,
            "iterations": 500,
            "resolution": (800, 800),
            "wing_ratio": 2.0,
            "symmetry": 0.9,
            "density": 0.5,
            "color_scheme": "rainbow",
            "seed": None
        }
        
        try:
            # Check if pawprint data has fractal analysis
            if "fractal_analysis" in pawprint_data:
                fractal = pawprint_data["fractal_analysis"]
                
                # Extract fractal dimension
                if "fractal_dimension" in fractal:
                    params["fractal_dimension"] = fractal["fractal_dimension"]
                
                # Extract other parameters
                if "self_similarity" in fractal:
                    # Use self-similarity to influence density
                    params["density"] = fractal["self_similarity"]
                
                # Extract butterfly parameters
                if "butterfly_parameters" in fractal:
                    butterfly = fractal["butterfly_parameters"]
                    
                    if "wing_ratio" in butterfly:
                        params["wing_ratio"] = butterfly["wing_ratio"]
                        
                    if "symmetry_score" in butterfly:
                        params["symmetry"] = butterfly["symmetry_score"]
                        
                    if "pattern_density" in butterfly:
                        params["density"] = butterfly["pattern_density"]
            
            # Extract complexity metrics
            if ("fractal_analysis" in pawprint_data and 
                "complexity_metrics" in pawprint_data["fractal_analysis"]):
                
                complexity = pawprint_data["fractal_analysis"]["complexity_metrics"]
                
                # Use correlation dimension to influence iterations
                if "correlation_dimension" in complexity:
                    # Scale iterations based on correlation dimension
                    dim = complexity["correlation_dimension"]
                    params["iterations"] = int(300 + 200 * dim)
            
            # Use metadata for seed if available
            if "metadata" in pawprint_data:
                meta = pawprint_data["metadata"]
                
                if "generation_time_ms" in meta:
                    # Use generation time as seed
                    params["seed"] = meta["generation_time_ms"]
            
            # Extract general properties that might influence color scheme
            if "summary" in pawprint_data:
                summary = pawprint_data["summary"]
                
                if "complexity_score" in summary:
                    # Select color scheme based on complexity
                    complexity = summary["complexity_score"]
                    
                    if complexity < 0.3:
                        params["color_scheme"] = "grayscale"
                    elif complexity < 0.5:
                        params["color_scheme"] = "bluescale"
                    elif complexity < 0.7:
                        params["color_scheme"] = "heatmap"
                    else:
                        params["color_scheme"] = "cosmic"
            
            logger.debug(f"Extracted parameters: {params}")
            return params
            
        except Exception as e:
            logger.error(f"Error extracting parameters from pawprint: {e}")
            return params
    
    def create_seed_from_pawprint(self, pawprint_data: Dict[str, Any]) -> int:
        """
        Create a seed value from pawprint data
        
        Args:
            pawprint_data: Dictionary containing pawprint data
            
        Returns:
            Integer seed value
        """
        # Start with a default seed
        seed = 42
        
        try:
            # Use primary hash if available
            if ("fingerprints" in pawprint_data and 
                "primary" in pawprint_data["fingerprints"]):
                
                primary = pawprint_data["fingerprints"]["primary"]
                
                if "hash" in primary:
                    # Convert hash to seed
                    hash_str = primary["hash"]
                    # Use first 8 characters of hash as hexadecimal number
                    seed = int(hash_str[:8], 16) % 1000000
            
            # Fallback to other values
            elif "metadata" in pawprint_data:
                meta = pawprint_data["metadata"]
                
                if "generation_time_ms" in meta:
                    seed = meta["generation_time_ms"]
                    
            # Use pattern count as additional influence
            if "patterns" in pawprint_data:
                patterns = pawprint_data["patterns"]
                seed += len(patterns) * 1000
            
            logger.debug(f"Created seed value: {seed}")
            return seed
            
        except Exception as e:
            logger.error(f"Error creating seed from pawprint: {e}")
            return seed
    
    def extract_pattern_data(self, pawprint_data: Dict[str, Any]) -> Optional[np.ndarray]:
        """
        Extract pattern data from pawprint for visualization
        
        Args:
            pawprint_data: Dictionary containing pawprint data
            
        Returns:
            Numpy array of pattern data or None if not available
        """
        try:
            if "patterns" not in pawprint_data:
                return None
                
            patterns = pawprint_data["patterns"]
            
            # Extract pattern scores and types
            scores = []
            types = []
            
            for pattern in patterns:
                if "score" in pattern:
                    scores.append(pattern["score"])
                if "type" in pattern:
                    types.append(pattern["type"])
            
            # Create a matrix of pattern influences
            if scores:
                # Create a 2D matrix where each cell is influenced by pattern scores
                size = max(10, len(scores))
                pattern_data = np.zeros((size, size))
                
                # Fill the matrix with pattern influences
                for i in range(size):
                    for j in range(size):
                        # Use pattern scores to influence values
                        for k, score in enumerate(scores):
                            # Create a radial pattern centered on different positions
                            center_x = size * (k % 3) / 3
                            center_y = size * (k // 3) / 3
                            
                            # Distance from center
                            dist = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                            
                            # Add influence based on distance and score
                            influence = score * np.exp(-dist / (size/4))
                            pattern_data[i, j] += influence
                
                # Normalize
                if np.max(pattern_data) > 0:
                    pattern_data = pattern_data / np.max(pattern_data)
                
                return pattern_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting pattern data: {e}")
            return None
    
    def load_pawprint_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load pawprint data from file
        
        Args:
            file_path: Path to pawprint file
            
        Returns:
            Dictionary containing pawprint data or None if error
        """
        try:
            logger.info(f"Loading pawprint file: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            # Load JSON data
            with open(file_path, 'r') as f:
                pawprint_data = json.load(f)
            
            logger.debug(f"Loaded pawprint file with {len(pawprint_data)} keys")
            return pawprint_data
            
        except Exception as e:
            logger.error(f"Error loading pawprint file: {e}")
            return None
