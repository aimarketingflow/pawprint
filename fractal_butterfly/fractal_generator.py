#!/usr/bin/env python3
"""
Fractal Generator Module

Generates fractal butterfly patterns for visualization.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import math
import logging
import numpy as np
from typing import Dict, Any, Tuple, List, Optional, Union

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.generator")

class FractalGenerator:
    """
    Generates fractal patterns for visualization
    """
    
    def __init__(self):
        """Initialize the fractal generator"""
        # Default parameters
        self.params = {
            "fractal_dimension": 1.5,
            "iterations": 500,
            "resolution": (800, 800),
            "wing_ratio": 2.0,
            "symmetry": 0.9,
            "density": 0.5,
            "color_scheme": "rainbow",
            "use_base_fractal": False,
            "base_fractal_influence": 0.5,
            "base_fractal_pattern": "mandelbrot"
        }
        
        # Available base fractal patterns
        self.base_patterns = {
            "mandelbrot": self._generate_mandelbrot,
            "julia": self._generate_julia,
            "burning_ship": self._generate_burning_ship,
            "tricorn": self._generate_tricorn,
            "multibrot": self._generate_multibrot
        }
        
        # Base fractal cache
        self.base_fractal_cache = {}
    
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """
        Set generation parameters
        
        Args:
            params: Dictionary of parameters
        """
        # Update parameters
        for key, value in params.items():
            if key in self.params:
                self.params[key] = value
        
        # Log parameter update
        logger.info(f"Updated fractal parameters: {', '.join(f'{k}={v}' for k, v in params.items())}")
        
        # Clear cache if base fractal parameters changed
        base_fractal_keys = ["use_base_fractal", "base_fractal_pattern", "base_fractal_influence"]
        if any(key in params for key in base_fractal_keys):
            self.base_fractal_cache = {}
            logger.debug("Cleared base fractal cache due to parameter changes")
    
    def generate_butterfly(self) -> Tuple[np.ndarray, List[Tuple[float, float, float]]]:
        """
        Generate a fractal butterfly pattern
        
        Returns:
            Tuple of (fractal data array, color list)
        """
        # Extract parameters
        dimension = self.params["fractal_dimension"]
        iterations = self.params["iterations"]
        resolution = self.params["resolution"]
        wing_ratio = self.params["wing_ratio"]
        symmetry = self.params["symmetry"]
        density = self.params["density"]
        color_scheme = self.params["color_scheme"]
        use_base_fractal = self.params["use_base_fractal"]
        base_fractal_influence = self.params["base_fractal_influence"]
        base_pattern = self.params["base_fractal_pattern"]
        
        # Log generation start
        logger.info(f"Generating fractal butterfly with dimension={dimension}, iterations={iterations}")
        logger.debug(f"Additional params: wing_ratio={wing_ratio}, symmetry={symmetry}, density={density}")
        
        # Generate base fractal if needed
        base_fractal = None
        if use_base_fractal:
            logger.info(f"Using base fractal pattern: {base_pattern} with influence={base_fractal_influence}")
            base_fractal = self._get_base_fractal(base_pattern, resolution)
        
        # Generate raw fractal data
        fractal_data = self._generate_fractal_data(
            dimension, iterations, resolution, wing_ratio, symmetry, density, base_fractal, base_fractal_influence
        )
        
        # Generate color scheme
        colors = self._generate_color_scheme(color_scheme, iterations)
        
        # Log generation completion
        logger.info(f"Generated fractal butterfly with shape {fractal_data.shape}")
        
        return fractal_data, colors
    
    def _get_base_fractal(self, pattern_name: str, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Get or generate a base fractal pattern
        
        Args:
            pattern_name: Name of the base fractal pattern
            resolution: Resolution (width, height)
            
        Returns:
            Base fractal data array
        """
        # Check cache first
        cache_key = f"{pattern_name}_{resolution[0]}x{resolution[1]}"
        if cache_key in self.base_fractal_cache:
            logger.debug(f"Using cached base fractal: {pattern_name}")
            return self.base_fractal_cache[cache_key]
        
        # Generate base fractal pattern
        if pattern_name in self.base_patterns:
            logger.info(f"Generating base fractal pattern: {pattern_name}")
            base_fractal = self.base_patterns[pattern_name](resolution)
            
            # Cache the result
            self.base_fractal_cache[cache_key] = base_fractal
            return base_fractal
        else:
            logger.warning(f"Unknown base fractal pattern: {pattern_name}, using mandelbrot")
            return self._generate_mandelbrot(resolution)
    
    def _generate_fractal_data(self, 
                              dimension: float, 
                              iterations: int, 
                              resolution: Tuple[int, int], 
                              wing_ratio: float, 
                              symmetry: float, 
                              density: float,
                              base_fractal: Optional[np.ndarray] = None,
                              base_influence: float = 0.5) -> np.ndarray:
        """
        Generate fractal data
        
        Args:
            dimension: Fractal dimension
            iterations: Maximum iterations
            resolution: Resolution (width, height)
            wing_ratio: Ratio between wings
            symmetry: Symmetry factor
            density: Density factor
            base_fractal: Optional base fractal to align with
            base_influence: Influence of base fractal (0-1)
            
        Returns:
            Fractal data array
        """
        # Create coordinate grid
        width, height = resolution
        x = np.linspace(-2, 1, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        c = X + 1j * Y
        
        # Initialize z and fractal data
        z = np.zeros_like(c)
        fractal_data = np.zeros_like(X, dtype=np.float64)
        
        # Adjust c based on parameters
        c_left = c * wing_ratio  # Left wing
        c_right = c * (1 / wing_ratio)  # Right wing
        
        # Apply symmetry factor
        mask_left = X < 0
        mask_right = X >= 0
        c[mask_left] = c_left[mask_left]
        c[mask_right] = c_right[mask_right] * (1 - symmetry) + np.conj(c_left[mask_right]) * symmetry
        
        # Adjust for fractal dimension
        power = 2.0 + (dimension - 1.5)  # Scale from 1.0 to 2.0 -> 1.5 to 2.5
        
        # Apply density factor
        escape_radius = 2.0 + 10.0 * density
        
        # Main iteration loop
        for i in range(iterations):
            # Apply fractal iteration
            z = z**power + c
            
            # Find points that escape this iteration
            mask = (fractal_data == 0) & (np.abs(z) > escape_radius)
            fractal_data[mask] = i
        
        # Set unescaped points to max iteration
        fractal_data[fractal_data == 0] = iterations
        
        # Apply base fractal if provided
        if base_fractal is not None:
            # Ensure base_fractal has same shape as fractal_data
            if base_fractal.shape != fractal_data.shape:
                logger.warning(f"Base fractal shape {base_fractal.shape} doesn't match fractal data {fractal_data.shape}")
                # Resize base fractal if needed
                base_fractal = np.resize(base_fractal, fractal_data.shape)
            
            # Normalize both fractals to 0-1 range for blending
            norm_base = (base_fractal - base_fractal.min()) / (base_fractal.max() - base_fractal.min())
            norm_fractal = (fractal_data - fractal_data.min()) / (fractal_data.max() - fractal_data.min())
            
            # Blend fractals based on influence factor
            blended = norm_fractal * (1 - base_influence) + norm_base * base_influence
            
            # Scale back to iteration range
            fractal_data = blended * iterations
        
        return fractal_data
    
    def _generate_color_scheme(self, scheme: str, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate a color scheme
        
        Args:
            scheme: Color scheme name
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        if scheme == "rainbow":
            return self._rainbow_colors(iterations)
        elif scheme == "bluescale":
            return self._blue_colors(iterations)
        elif scheme == "heatmap":
            return self._heat_colors(iterations)
        elif scheme == "grayscale":
            return self._gray_colors(iterations)
        elif scheme == "cosmic":
            return self._cosmic_colors(iterations)
        else:
            logger.warning(f"Unknown color scheme: {scheme}, using rainbow")
            return self._rainbow_colors(iterations)
    
    def _rainbow_colors(self, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate rainbow color scheme
        
        Args:
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        colors = []
        for i in range(iterations + 1):
            # Convert to 0-1 range
            t = i / iterations
            
            # Rainbow color calculation
            r = 0.5 + 0.5 * np.sin(np.pi * t)
            g = 0.5 + 0.5 * np.sin(np.pi * t + 2 * np.pi / 3)
            b = 0.5 + 0.5 * np.sin(np.pi * t + 4 * np.pi / 3)
            
            colors.append((r, g, b))
        
        return colors
    
    def _blue_colors(self, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate blue color scheme
        
        Args:
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        colors = []
        for i in range(iterations + 1):
            # Convert to 0-1 range
            t = i / iterations
            
            # Blue scale color calculation
            r = 0.0
            g = t * 0.6
            b = 0.4 + t * 0.6
            
            colors.append((r, g, b))
        
        return colors
    
    def _heat_colors(self, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate heat map color scheme
        
        Args:
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        colors = []
        for i in range(iterations + 1):
            # Convert to 0-1 range
            t = i / iterations
            
            # Heat map color calculation
            r = min(1.0, t * 3)
            g = max(0.0, min(1.0, t * 3 - 1))
            b = max(0.0, min(1.0, t * 3 - 2))
            
            colors.append((r, g, b))
        
        return colors
    
    def _gray_colors(self, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate grayscale color scheme
        
        Args:
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        colors = []
        for i in range(iterations + 1):
            # Convert to 0-1 range
            t = i / iterations
            
            # Grayscale color calculation
            gray = t
            
            colors.append((gray, gray, gray))
        
        return colors
    
    def _cosmic_colors(self, iterations: int) -> List[Tuple[float, float, float]]:
        """
        Generate cosmic color scheme
        
        Args:
            iterations: Maximum iterations
            
        Returns:
            List of RGB color tuples
        """
        colors = []
        for i in range(iterations + 1):
            # Convert to 0-1 range
            t = i / iterations
            
            # Cosmic color calculation
            r = 0.5 + 0.5 * np.sin(np.pi * t * 3)
            g = 0.5 + 0.5 * np.sin(np.pi * t * 5)
            b = 0.5 + 0.5 * np.sin(np.pi * t * 7 + np.pi / 2)
            
            colors.append((r, g, b))
        
        return colors
    
    def _generate_mandelbrot(self, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Generate Mandelbrot set fractal
        
        Args:
            resolution: Resolution (width, height)
            
        Returns:
            Fractal data array
        """
        width, height = resolution
        x = np.linspace(-2, 1, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        c = X + 1j * Y
        z = np.zeros_like(c)
        
        iterations = 100
        fractal = np.zeros_like(X, dtype=np.float64)
        
        for i in range(iterations):
            mask = (fractal == 0) & (np.abs(z) < 2.0)
            z[mask] = z[mask]**2 + c[mask]
            fractal[mask & (np.abs(z) > 2.0)] = i
        
        fractal[fractal == 0] = iterations
        return fractal
    
    def _generate_julia(self, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Generate Julia set fractal
        
        Args:
            resolution: Resolution (width, height)
            
        Returns:
            Fractal data array
        """
        width, height = resolution
        x = np.linspace(-2, 2, width)
        y = np.linspace(-2, 2, height)
        X, Y = np.meshgrid(x, y)
        z = X + 1j * Y
        c = -0.8 + 0.156j  # Julia set parameter
        
        iterations = 100
        fractal = np.zeros_like(X, dtype=np.float64)
        
        for i in range(iterations):
            mask = (fractal == 0) & (np.abs(z) < 2.0)
            z[mask] = z[mask]**2 + c
            fractal[mask & (np.abs(z) > 2.0)] = i
        
        fractal[fractal == 0] = iterations
        return fractal
    
    def _generate_burning_ship(self, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Generate Burning Ship fractal
        
        Args:
            resolution: Resolution (width, height)
            
        Returns:
            Fractal data array
        """
        width, height = resolution
        x = np.linspace(-2, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        c = X + 1j * Y
        z = np.zeros_like(c)
        
        iterations = 100
        fractal = np.zeros_like(X, dtype=np.float64)
        
        for i in range(iterations):
            mask = (fractal == 0) & (np.abs(z) < 2.0)
            z_real = np.abs(z.real)
            z_imag = np.abs(z.imag)
            z[mask] = (z_real + 1j * z_imag)**2 + c[mask]
            fractal[mask & (np.abs(z) > 2.0)] = i
        
        fractal[fractal == 0] = iterations
        return fractal
    
    def _generate_tricorn(self, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Generate Tricorn fractal
        
        Args:
            resolution: Resolution (width, height)
            
        Returns:
            Fractal data array
        """
        width, height = resolution
        x = np.linspace(-2, 1, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        c = X + 1j * Y
        z = np.zeros_like(c)
        
        iterations = 100
        fractal = np.zeros_like(X, dtype=np.float64)
        
        for i in range(iterations):
            mask = (fractal == 0) & (np.abs(z) < 2.0)
            z[mask] = np.conj(z[mask])**2 + c[mask]
            fractal[mask & (np.abs(z) > 2.0)] = i
        
        fractal[fractal == 0] = iterations
        return fractal
    
    def _generate_multibrot(self, resolution: Tuple[int, int]) -> np.ndarray:
        """
        Generate Multibrot fractal
        
        Args:
            resolution: Resolution (width, height)
            
        Returns:
            Fractal data array
        """
        width, height = resolution
        x = np.linspace(-2, 1, width)
        y = np.linspace(-1.5, 1.5, height)
        X, Y = np.meshgrid(x, y)
        c = X + 1j * Y
        z = np.zeros_like(c)
        
        power = 3  # Higher power for multibrot
        iterations = 100
        fractal = np.zeros_like(X, dtype=np.float64)
        
        for i in range(iterations):
            mask = (fractal == 0) & (np.abs(z) < 2.0)
            z[mask] = z[mask]**power + c[mask]
            fractal[mask & (np.abs(z) > 2.0)] = i
        
        fractal[fractal == 0] = iterations
        return fractal
