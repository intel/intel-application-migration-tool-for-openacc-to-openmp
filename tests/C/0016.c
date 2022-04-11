float foo (int N, float vec[])
{
	int VECLEN = 4;

	#pragma acc parallel loop num_workers(10) copy(vec[:N])
	for (int i = 0; i < N; ++i)
		vec[i] = i + 1.;

	#pragma acc parallel num_gangs(2) copy(vec[:N])
	#pragma acc loop gang
	for (int i = 0; i < N; ++i)
		vec[i] = i + 2.;

	#pragma acc parallel num_gangs(2) num_workers(10) copy(vec[:N])
	#pragma acc loop
	for (int i = 0; i < N; ++i)
		vec[i] = i + 3.;

	#pragma acc parallel num_gangs(2) copy(vec[:N]) if(1==1)
	#pragma acc loop vector
	for (int i = 0; i < N; ++i)
		vec[i] = i + 4.;

	#pragma acc parallel loop vector vector_length(VECLEN)
	for (int i = 0; i < N; ++i)
		vec[i] = i + 4.;

	return vec[N-1];
}
