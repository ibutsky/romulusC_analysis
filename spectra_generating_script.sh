mpirun -np 1 python generate_spectra.py 1 3 3035 &> estd0.out &\
mpirun -np 1 python generate_spectra.py 3 5 3035 &> estd3.out &\
mpirun -np 1 python generate_spectra.py 5 7 3035 &> estd5.out &\
mpirun -np 1 python generate_spectra.py 7 9 3035 &> estd7.out &\
mpirun -np 1 python generate_spectra.py 9 11 3035 &> estd9.out 


