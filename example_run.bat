::python pso_algorithm.py case14 50 20 0.25 0.2 0.7 particles20run1
::python pso_algorithm.py case14 50 20 0.25 0.2 0.7 particles20run2
::python pso_algorithm.py case14 50 20 0.25 0.2 0.7 particles20run3

::python pso_algorithm.py case14 50 60 0.25 0.2 0.7 particles60run1
::python pso_algorithm.py case14 50 60 0.25 0.2 0.7 particles60run2
::python pso_algorithm.py case14 50 60 0.25 0.2 0.7 particles60run3

::python pso_algorithm.py case14 50 100 0.25 0.2 0.7 particles100run1
::python pso_algorithm.py case14 50 100 0.25 0.2 0.7 particles100run2
::python pso_algorithm.py case14 50 100 0.25 0.2 0.7 particles100run3

::python pso_algorithm.py case14 50 140 0.25 0.2 0.7 particles140run1
::python pso_algorithm.py case14 50 140 0.25 0.2 0.7 particles140run2
::python pso_algorithm.py case14 50 140 0.25 0.2 0.7 particles140run3

::python pso_algorithm.py case14 50 180 0.25 0.2 0.7 particles180run1
::python pso_algorithm.py case14 50 180 0.25 0.2 0.7 particles180run2
::python pso_algorithm.py case14 50 180 0.25 0.2 0.7 particles180run3


python pso_algorithm_profiled.py "" 50 20 0.25 0.2 0.7 particles20run1
python pso_algorithm_profiled.py "" 50 60 0.25 0.2 0.7 particles60run1
python pso_algorithm_profiled.py "" 50 100 0.25 0.2 0.7 particles100run1
python pso_algorithm_profiled.py "" 50 140 0.25 0.2 0.7 particles140run1
python pso_algorithm_profiled.py "" 50 180 0.25 0.2 0.7 particles180run1


pause
