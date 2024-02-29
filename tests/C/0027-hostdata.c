int main()
{
	int a[1000],b[1000];
	#pragma acc data copyin(a,b)
	{
		#pragma acc kernels
		{
			for (int i = 0; i < 1000; ++i)
				a[i] = i;
		}
		#pragma acc host_data use_device(a,b)
		{
		}
	}
	return 0;
}
