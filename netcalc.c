/*
 * This is a simple tool to give a range of addresses as well as the validity of
 * a network mask (lax, post-CIDR shennanigans) from any of binary, decimal or
 * CIDR notation.
 *
 * ISC masterrace - look at ./LICENSE
 *
 * dami0 (at) iotek (dot) com
 * IOTek represent
 * Copyright 2014, to infinity and beyond to the other end of the scale
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int to10(char *bin, size_t siz) {

	int i, j;
	int sum = 0;

	/* this is a conversion of (single) char to int, summed */
	for (i = 0, j = siz - 1; i < siz; i++, j--) {
		sum += (bin[i] - '0')*pow(2, j);
	}
	return sum;
}

int to2(int n) {

	int i, j;
	int d;
	int siz;

	if (n == 0) return 0;

	for (j = 1, d = 0; d <= n; j++) d = pow(2, j);
	siz = j - 1;
	char *tmp;
	if ( NULL == (tmp = malloc(siz*sizeof(char))) ) {
		printf("malloc failed\n");
		return -1;
	}
	for (i = 0; i < siz; i++) tmp[i] = '0'; tmp[0] = '1';

	for (i = 1; n > 1; i++) {
		n -= d*0.5;
		if (n == 0) break;
		for (j = 0, d = 0; d <= n; j++) d = pow(2, j);
		tmp[siz - j + 1] = '1';
	}
	return atoi(tmp);
	free(tmp);
}

int dec(char *nm) {

	int out[4];
	int i, j, k;
	int dels[5];
	char tmp[3] = "000";

	dels[0] = -1;
	for (i = 0, j = 1; i < 18; i++) {
		if (nm[i] == '.') {
			dels[j++] = i;
			if ((dels[j-1] - dels[j-2]) > 4) return -1;
		}
		if (nm[i] == '\0') dels[j] = i;
//		if ((dels[j] - dels[j-1]) > 5) { printf("kakakak"); return -1; }
	}
	printf("%i.%i.%i.%i 3\n", dels[0], dels[1], dels[2], dels[3]);

	for (i = 0; i < 4; i++) {
		for (j = 0; j < 3; j++) tmp[j] = '0';
		for (k = 2, j = dels[i+1] - 1; j > dels[i]; j--, k--) {
			tmp[k] = nm[j];
		}
		printf("%s 2\n", tmp);
		out[i] = atoi(tmp);
	}

//	printf("%i.%i.%i.%i\n", dels[0], dels[1], dels[2], dels[3]);

	return 0;
}

int main(int argc, char **argv) {

	int i;
	char *nmask;

	nmask = argv[1];
	printf("%s 1\n", nmask);
	dec(nmask);

	return 0;
}
