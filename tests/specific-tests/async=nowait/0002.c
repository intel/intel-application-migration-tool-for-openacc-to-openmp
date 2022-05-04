int main (int argc, char *argv[])
{
	int x;

	#pragma acc parallel async(1)
	{
	x = 1;
	}

	_Pragma("acc parallel async(2)")
	{
	x = 2;
	}

	_Pragma("acc \
	 parallel async(3)")
	{
	x = 3;
	}

	#pragma acc wait (3)
	#pragma acc wait
}
