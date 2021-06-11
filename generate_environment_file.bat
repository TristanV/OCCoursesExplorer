echo Execute this bat file from CMD Prompt when running the Conda environment that you need to export 

echo Generating environment file for conda
conda env export > environment.yml

echo Generating environment file for pip
pip freeze > requirements.txt

pause