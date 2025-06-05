#!/usr/bin/env python3
"""
Fractal Metrics Calculator Module

Calculates metrics and statistics from fractal butterfly patterns.

Author: AIMF LLC
Date: June 2, 2025
"""

import logging
import numpy as np
from typing import Dict, Any, List, Tuple, Optional

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.metrics")

class MetricsCalculator:
    """
    Class for calculating metrics from fractal butterfly patterns
    """
    
    def __init__(self):
        """Initialize the metrics calculator"""
        pass
    
    def calculate_all_metrics(self, fractal_data: np.ndarray) -> Dict[str, Any]:
        """
        Calculate all metrics from fractal data
        
        Args:
            fractal_data: Numpy array containing fractal data
            
        Returns:
            Dictionary of calculated metrics
        """
        logger.info("Calculating fractal metrics")
        
        metrics = {}
        
        # Basic statistics
        metrics["min"] = float(np.min(fractal_data))
        metrics["max"] = float(np.max(fractal_data))
        metrics["mean"] = float(np.mean(fractal_data))
        metrics["median"] = float(np.median(fractal_data))
        metrics["std_dev"] = float(np.std(fractal_data))
        
        # Fractal dimension estimation
        metrics["fractal_dimension"] = self.estimate_fractal_dimension(fractal_data)
        
        # Pattern metrics
        metrics["symmetry_score"] = self.calculate_symmetry(fractal_data)
        metrics["complexity"] = self.calculate_complexity(fractal_data)
        metrics["entropy"] = self.calculate_entropy(fractal_data)
        
        # Advanced metrics
        metrics["hurst_exponent"] = self.estimate_hurst_exponent(fractal_data)
        metrics["lyapunov_exponent"] = self.estimate_lyapunov_exponent(fractal_data)
        
        logger.debug(f"Metrics calculated: {metrics}")
        return metrics
    
    def estimate_fractal_dimension(self, fractal_data: np.ndarray) -> float:
        """
        Estimate fractal dimension using box-counting method
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Estimated fractal dimension
        """
        # Simplified box-counting implementation
        # In a real implementation, this would use a more sophisticated algorithm
        
        # Normalize data
        normalized = (fractal_data - np.min(fractal_data)) / (np.max(fractal_data) - np.min(fractal_data))
        
        # Threshold to create binary image
        binary = normalized > 0.5
        
        # Count boxes at different scales
        scales = [2, 4, 8, 16, 32]
        counts = []
        
        for scale in scales:
            # Downsample by taking max in each box
            h, w = binary.shape
            box_count = 0
            
            for i in range(0, h, scale):
                for j in range(0, w, scale):
                    # Get box
                    box = binary[i:min(i+scale, h), j:min(j+scale, w)]
                    if np.any(box):
                        box_count += 1
                        
            counts.append(box_count)
        
        # Calculate dimension as slope of log(count) vs log(1/scale)
        log_scales = np.log([1/s for s in scales])
        log_counts = np.log(counts)
        
        # Linear regression to find slope
        if len(log_scales) > 1:
            slope = np.polyfit(log_scales, log_counts, 1)[0]
        else:
            slope = 1.0
            
        return float(slope)
    
    def calculate_symmetry(self, fractal_data: np.ndarray) -> float:
        """
        Calculate symmetry score (0-1)
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Symmetry score between 0 and 1
        """
        h, w = fractal_data.shape
        
        # Compare left and right halves
        mid = w // 2
        left = fractal_data[:, :mid]
        right = fractal_data[:, mid:]
        
        # Flip right side for comparison
        right_flipped = np.fliplr(right)
        
        # Trim to same size if necessary
        min_width = min(left.shape[1], right_flipped.shape[1])
        left = left[:, :min_width]
        right_flipped = right_flipped[:, :min_width]
        
        # Calculate difference
        diff = np.abs(left - right_flipped)
        max_diff = np.max(fractal_data) - np.min(fractal_data)
        
        if max_diff == 0:
            return 1.0
            
        # Calculate symmetry score (1 = perfect symmetry)
        symmetry = 1.0 - (np.mean(diff) / max_diff)
        
        return float(symmetry)
    
    def calculate_complexity(self, fractal_data: np.ndarray) -> float:
        """
        Calculate complexity score (0-1)
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Complexity score between 0 and 1
        """
        # Use gradient magnitude as a measure of complexity
        gx, gy = np.gradient(fractal_data)
        gradient_magnitude = np.sqrt(gx**2 + gy**2)
        
        # Normalize
        complexity = np.mean(gradient_magnitude) / (np.max(fractal_data) - np.min(fractal_data))
        
        # Scale to 0-1
        complexity = min(max(complexity, 0.0), 1.0)
        
        return float(complexity)
    
    def calculate_entropy(self, fractal_data: np.ndarray) -> float:
        """
        Calculate entropy
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Entropy value
        """
        # Normalize data to 0-1
        normalized = (fractal_data - np.min(fractal_data)) / (np.max(fractal_data) - np.min(fractal_data))
        
        # Bin data into histogram
        hist, _ = np.histogram(normalized, bins=50, density=True)
        
        # Remove zeros
        hist = hist[hist > 0]
        
        # Calculate entropy
        entropy = -np.sum(hist * np.log2(hist))
        
        # Normalize to 0-1
        max_entropy = np.log2(50)  # Maximum possible entropy with 50 bins
        normalized_entropy = entropy / max_entropy
        
        return float(normalized_entropy)
    
    def estimate_hurst_exponent(self, fractal_data: np.ndarray) -> float:
        """
        Estimate Hurst exponent
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Estimated Hurst exponent
        """
        # Simple estimation - in real implementation, this would be more sophisticated
        # Use the central row of the fractal as a time series
        middle_row = fractal_data[fractal_data.shape[0]//2, :]
        
        # Calculate differences
        differences = np.diff(middle_row)
        
        # Calculate variance of differences
        variance = np.var(differences)
        
        # Simplified Hurst calculation
        # H = 0.5 is random, H > 0.5 is persistent, H < 0.5 is anti-persistent
        if variance == 0:
            return 0.5
            
        # Normalize complexity to derive a Hurst-like value
        complexity = self.calculate_complexity(fractal_data)
        hurst = 0.5 + (complexity - 0.5) * 0.8
        
        return float(hurst)
    
    def estimate_lyapunov_exponent(self, fractal_data: np.ndarray) -> float:
        """
        Estimate Lyapunov exponent
        
        Args:
            fractal_data: Fractal data array
            
        Returns:
            Estimated Lyapunov exponent
        """
        # Simplified estimation - in real implementation would use more sophisticated algorithms
        # Positive Lyapunov exponent indicates chaos
        
        # Use entropy and complexity to derive a Lyapunov-like value
        entropy = self.calculate_entropy(fractal_data)
        complexity = self.calculate_complexity(fractal_data)
        
        # Combine metrics to estimate Lyapunov exponent
        lyapunov = (entropy * complexity) * 0.2  # Scale to reasonable range
        
        return float(lyapunov)
