echo OFF
echo "this batch or its Voila command line should be launched within the Python virtual environment OCCoursesExplorer satisfying all dependencies described in requirements.txt"
voila --enable_nbextensions=True --VoilaConfiguration.file_whitelist="['.*\.(csv|html|png|jpg)', 'viz.*', 'data.*']" OCCoursesExplorer.ipynb

