int main (int argc, char*argv[])
{
	unsigned N = 1000;
	unsigned a[N],b[N];

	#pragma acc kernels copyout(a[0:N])
	{
		#pragma acc loop
		for (unsigned i = 0; i < N; ++i)
			a[i] = i+1;
	}
	#pragma acc kernels copyin(a[0:N]) copyout(b[0:N])
	{
		#pragma acc loop
		for (unsigned i = 0; i < N; ++i)
			b[i] = a[i] + 1;
	}
	#pragma acc kernels copyin(a[0:N]) copyout(b[0:N])
	{
		#pragma acc loop
		for (unsigned i = 0; i < N; ++i)
			a[i] = i + 1;
		#pragma acc loop
		for (unsigned i = 0; i < N; ++i)
			b[i] = a[i] + 1;
	}
	#pragma acc kernels loop copyin(a[0:N]) copyout(b[0:N])
	for (unsigned i = 0; i < N; ++i)
		b[i] = a[i] + 1;

	return 0;
}
