int foo (int a, int b)
{
	#pragma acc parallel copyin(a) copyin(b)
	#pragma omp target teams map(to:a,b)
	{
	}

	#pragma acc parallel copy(a) copy(b)
	#pragma omp target teams \
	  map(a,b)
	{
	}

	#pragma acc parallel copy(a) copy(b)
	#pragma omp \
	  target \
	  teams \
	  map(a,b)
	{
	}

	int r = 0;
	#pragma acc parallel copy(a)
	#pragma acc loop reduction(+:r)
	#pragma omp target teams
	#pragma omp loop reduction(+:r)
	for (int i = a; i < b; ++i)
		r += i*i;

	return r;
}
