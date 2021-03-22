set /p file_to_copy="Specify the file to be copied: "
set /p destination_directory="specify the destination directory: "
scp %file_to_copy% s1895870@login.cirrus.ac.uk:/lustre/home/dc116/s1895870/%destination_directory%
pause
