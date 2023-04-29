# MDMA

Material Defect Measurement Analyzer

### Project uses pyton interpreter in version 3.11

# Installation

1. Set up python virtual environment
2. Download requirements using command

    ```s
    pip install -r requirements.txt
    ```

3. Make sure '.env' file is located in root dir and contains following definitions:

    ```s
   VERSION=2.0.1               # <- describes current version of MDMA aplication
   #PRINTED_MODE=mock_printer  # <- specifies whether MDMA should use mock printer device
   #ANALYZER_MODE=mock_hameg   # <- specifies whether MDMA should use mock analyzer device 
                                # use 'mock_hameg' for HamegHMS3010 devce
                                # use 'pocket_vna' for PocketVNA devce
    ```

# Developer guide

1. Used auto-formatter: Black (installed via pip command)
2. Used linter: ruff (installed via pip command) and SonarLint (pycharm plugin)
3. Top generate executable application from python script run following:
    ```s
    pip install pyinstaller

    pyinstaller --onefile --noconsole  .\src\app_main.py
    ```

# Problems with previous solution, and how to fix them

1. Plotting was slow...
2. Measurement data was hard to name, save and retain
3. Code sucked
4. No unit testing
5. No way to test the correct behaviour of device
6. Working on UI was difficult
7. A lot of prep work was required before each scan