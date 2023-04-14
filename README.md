# MDMA

Material Defect Measurement Analyzer

# Problems with previous solution, and how to fix them

1. Plotting was slow...
2. Measurement data was hard to name, save and retain
3. Code sucked, bad implementation and paches on top of paches
4. No unit testing
5. No way to test the correct behaviour of device
6. Working on UI was difficult
7. A lot of prep work was required before each scan

to convert python script to .exe app run following:

    pip install pyinstaller

    pyinstaller --onefile --noconsole  .\src\app_main.py

