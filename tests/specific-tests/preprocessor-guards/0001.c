int main (int argc, char*argv[])
{
	int x;

	#pragma acc kernels
	{
		x = 2;
	}

	_Pragma("acc kernels")
	{
	x = 3;
	}

	_Pragma("acc \
	 kernels")
	{
	x = 4;
	}

	return 0;
}
