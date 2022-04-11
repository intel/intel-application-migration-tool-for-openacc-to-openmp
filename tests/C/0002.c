int main (int argc, char *argv[])
{
	int x;

	#pragma acc parallel
	{
	x = 1;
	}

	_Pragma("acc parallel")
	{
	x = 2;
	}

	_Pragma("acc \
	 parallel")
	{
	x = 3;
	}
}
