int main (int argc, char*argv[])
{
	int x;

	#pragma acc kernels async(1)
	{
		x = 2;
	}

	_Pragma("acc kernels async(2)")
	{
	x = 3;
	}

	_Pragma("acc \
	 kernels async(3) wait(1)")
	{
	x = 4;
	}

	#pragma acc wait(2)
	#pragma acc wait

	return 0;
}
