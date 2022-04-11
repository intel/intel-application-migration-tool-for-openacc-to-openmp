int main (int argc, char *argv[])
{
	#define N 10
	#define M 20
	#define O 30

	int x[N], Y[M], z[O];

	#pragma acc data present(x)
	{
	}

	#pragma acc data present(Y)
	{
	}

	#pragma acc data copy(x) \
	  copyin(Y) copyout(z)
	{
	}

	#pragma acc \
	data \
present(z)
	{
	}

	#pragma acc data \
  copy(x) copyin (Y) copyout (z)
	{
	}

	return 0;
}
