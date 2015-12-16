gcc outputapi.c -c
gcc -shared -o outputapi.dll *.o
gcc test.c -c
gcc -o test.exe test.o -L. -l outputapi -lm