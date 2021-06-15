echo Execute this bat file from CMD Prompt when running the Conda environment that you need to export 

echo Generating environment file for conda
conda env export --from-history > environment.yml 

pause