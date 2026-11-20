#include <stdio.h>
#include "pragma_acc.h"

int main(void)
{
	double accum = 0.0, vacc = 0.0, a[100];

	#pragma acc parallel loop copyout(a)
	for (int i = 0; i < 100; i++)
		a[i] = i;

	#pragma omp parallel for reduction(+:accum)
	for (int i = 0; i < 100; i++)
		accum += a[i];

	_Pragma("omp parallel for reduction(+:vacc)")
	for (int i = 0; i < 100; i++)
		vacc += a[i];

	_Pragma("acc parallel loop copy(a)")
	for (int i = 0; i < 100; i++)
		a[i] = a[i] * 2;

	printf("%f %f\n", accum, vacc);
	return 0;
}
