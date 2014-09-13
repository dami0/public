/*
 * This is a simple tool to give a range of addresses as well as the validity
 * of a network mask (lax, post-CIDR shennanigans) from any of binary, decimal
 * or CIDR notation.
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

int bin(char *nm) {

	int i;
	int out;
	int cnt;

	for (i = 0, out = 0, cnt = 1; i < 32; i++) {
		/* error handling */
		if (nm[i] != '1' && nm[i] != '0') {
			puts("Stop right there criminal scum!");
			return -1;
		} else if (nm[i+1] == '1' && nm[i] == '0') {
			puts("Invalid netmask; a one followed a zero");
			return -1;
		}

		/* actual calculation */
		if (nm[i] == '.') cnt++;
		if (nm[i] == '1') out++;
	}
	if (i < 32) {
		puts("Invalid netmask; not enough values");
		return -1;
	}

	return out;
}

int dec(char *nm) {

	int out[4];
	int i, j, k;
	char tmp[4];

	/* turn string into array of ints */
	for (i = 0, j = 0, k = 0; i < 16; i++) {
		if (nm[i] == '.' || i == 15) {
			tmp[j] = '\0';
			out[k++] = atoi(tmp);
			j = 0;
		} else { tmp[j++] = nm[i]; }
	}
	
	/* size does matter :( */
	if (k != 4) {
		puts("Illegal netmask; not enough values");
	}

	/* format appropriately for handling by next function */
	sprintf(nm, "%08i%08i%08i%08i", to2(out[0]), to2(out[1]),
			to2(out[2]), to2(out[3]));
	puts(nm);

	return bin(nm);
}

int main(int argc, char **argv) {

	int i;
	int cidr;
	long int j;
	char *mode;
	char *nmask;

	/* initialisations */
	i = 0;
	mode = argv[1];
	nmask = argv[2];

	/* pick which base/style number is presented in */
	if (mode[0] != '-') return -1;
	if (mode[1] == 'b') { i = 1;
	} else if (mode[1] == 'd') { i = 2;
	} else if (mode[1] == 'c') { i = 3; }

	/* act accordingly given previous code */
	switch (i) {
		case 0:
			cidr = -1;
			break;
		case 1:
			cidr = bin(nmask);
			break;
		case 2:
			cidr = dec(nmask);
			break;
		case 3:
			cidr = atoi(nmask);
			break;
	}

	/* print CIDR notation */
	if (cidr > -1) { printf("/%i\n", cidr);
	} else if (cidr < 0) { return -1; }

	/* print out information regarding number of networks */
	j = (long int) pow(2, cidr);
	printf("\nNetworks: %li\n", j);
	j = (long int) pow(2, 32 - cidr);
	printf("Hosts:    %li\n", j);
	/* go home for dinner */
	return 0;
}
