#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pawprinting PyQt6 - Pash Generation Flow Diagram Generator
Date: 2025-06-03

This script generates a diagram showing the flow of data in the Pawprinting PyQt6 application,
specifically focusing on the "Pash" (pawprint signature) generation process.

Requirements:
    - Python 3.6+
    - diagrams library (`pip install diagrams`)
    - Graphviz installed and in PATH

Usage:
    $ python3 pash_generation_diagram.py
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import React
from diagrams.programming.language import Python
from diagrams.generic.database import SQL
from diagrams.generic.storage import Storage
from diagrams.onprem.client import User
from diagrams.custom import Custom

# For custom icons not available in diagrams library
CUSTOM_ICON_PATH = "../resources/icons"

# Set to True to use custom icons if available
USE_CUSTOM_ICONS = False

def generate_diagram():
    """Generate the Pawprinting PyQt6 Pash Generation Flow diagram."""
    
    # Create diagram with appropriate styling
    with Diagram("Pawprinting PyQt6 - Pash Generation Flow", 
                 show=True, 
                 filename="pash_generation_flow",
                 outformat="png",
                 direction="TB"):  # TB = top to bottom
        
        # Define main actors
        user = User("User")
        
        # UI Layer
        with Cluster("UI Layer"):
            text_input = React("TextInputWidget")
            analyze_screen = React("AnalyzeScreen") 
            json_viewer = React("JsonViewerWidget")
        
        # Backend Layer
        with Cluster("Backend Layer"):
            converter = Python("TextToFractalConverter")
            
            # Subprocesses within the converter
            with Cluster("text_to_parameters Method"):
                hash_generation = Python("Standard Hash Generation\n(SHA256, SHA512)")
                pash_generation = Python("Pash Generation\n(5 points, 3 chars each)")
                fractal_params = Python("Fractal Parameters\nCalculation")
                params_dict = Python("Params Dictionary\nCreation")
        
        # Data Storage
        config_file = Storage("Saved Config\n(JSON)")
        
        # Draw flow arrows
        user >> Edge(label="Enter text") >> text_input
        text_input >> Edge(label="Generate Parameters") >> converter
        
        # Internal converter flow
        converter >> hash_generation
        hash_generation >> pash_generation
        pash_generation >> fractal_params
        fractal_params >> params_dict
        params_dict >> converter
        
        # Return path and save flow
        converter >> Edge(label="Return params") >> text_input
        text_input >> Edge(label="Save Configuration") >> config_file
        
        # Analysis flow
        user >> Edge(label="Load file") >> analyze_screen
        analyze_screen >> Edge(label="Read file") >> config_file
        analyze_screen >> Edge(label="Pass data") >> json_viewer
        json_viewer >> Edge(label="Display 'pawprint_signature'") >> user

if __name__ == "__main__":
    generate_diagram()
    print("Diagram generated: pash_generation_flow.png")
    print("The diagram has been saved in the current directory.")
