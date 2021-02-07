#!/usr/bin/env python
import os
from plumbum import local


if __name__ == "__main__":
    print("Launching streamlit...")
    try:
        local["streamlit"]["run", os.path.join(os.path.dirname(__file__), "TARAVisualize", "main.py")]()
    except KeyboardInterrupt:
        print("\nEnding streamlit...")
