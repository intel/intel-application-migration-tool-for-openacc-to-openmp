int main (int argc, char *argv[])
{
	unsigned N = 1000;

	#pragma acc parallel loop
	for (unsigned i = 0; i < N; ++i)
	{
	}

	#pragma \
	  acc parallel loop
	for (unsigned i = 0; i < N; ++i)
	{
	}

	  #pragma \
	    acc parallel loop
	for (unsigned i = 0; i < N; ++i)
	{
	}

	  #pragma \
	    acc \
	    parallel loop
	for (unsigned i = 0; i < N; ++i)
	{
	}

	  #pragma \
	    acc \
	    parallel \
	    loop
	for (unsigned i = 0; i < N; ++i)
	{
	}
	return 0;
}
