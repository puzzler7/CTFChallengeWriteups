#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    // if (argc < 2) {
    //     printf("Please enter a seed.\n");
    //     exit(-1);
    // }
    // srand(atoi(argv[1]));
    // printf("[");
    // for (int i = 0; i<10; i++) {
        printf("[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d]\n", rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand(), rand());
    // }
    // printf("]");
}
