import sys
import os
import core.app
from core.app import App

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        app = App()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
        
    
if __name__ == "__main__":
    main()
