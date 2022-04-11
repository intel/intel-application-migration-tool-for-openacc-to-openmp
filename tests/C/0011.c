float dot (int N, float * x, float * y)
{
	float tmp = 0;
	#pragma acc parallel loop reduction(+:tmp)
	for (int i = 0; i < N; ++i)
		tmp += x[i] * y[i];
	return tmp;
}

void dot2 (int N, float * x, float * y, float *d1, float *d2)
{
	float tmp1 = 0, tmp2 = 0;
	#pragma acc parallel loop reduction(+:tmp1) reduction(+:tmp2)
	for (int i = 0; i < N; ++i)
	{
		tmp1 += x[i] * y[i];
		tmp2 += y[i] * x[i];
	}
	*d1 = tmp1;
	*d2 = tmp2;
}
