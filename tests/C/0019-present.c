int main (void)
{
	unsigned v[10] = { 0 };

	#pragma acc data create(v)
	{
		#pragma acc parallel loop present(v)
		for (unsigned i = 0; i < 10; ++i)
			v[i] = i;
		#pragma acc update host(v)
	}

	#pragma acc data create(v)
	{
		#pragma acc parallel loop default(present)
		for (unsigned i = 0; i < 10; ++i)
			v[i] = 2*i;
		#pragma acc update host(v)
	}
	return 0;
}
