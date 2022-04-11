int main (int argc, char *argv[])
{
#define N 10
	int A[N];

	#pragma acc kernels
	{
		#pragma acc loop
		for (int i = 0; i < N; ++i)
			A[i] = i;
	}

	#pragma acc kernels loop
	for (int i = 0; i < N; ++i)
		A[i] = i;

	#pragma acc kernels
	#pragma acc loop
	for (int i = 0; i < N; ++i)
		A[i] = i;

	return 0;
}
