int main (int argc, char *argv[])
{
	#pragma acc kernels
	{
		int oneliner_stmt = 0;
		#pragma acc loop
		for (int i = 0; i < 10; ++i)
		{
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
			{
			}
		}
		#pragma acc loop
		for (int i = 0; i < 10; ++i)
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
				oneliner_stmt++;
		oneliner_stmt++;
		oneliner_stmt++;
		oneliner_stmt++;
		#pragma acc loop
		for (int i = 0; i < 10; ++i)
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
				#pragma acc loop
				for (int k = 0; k < 3; ++k)
					oneliner_stmt++;
		#pragma acc loop
		for (int i = 0; i < 10; ++i) {
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
				oneliner_stmt++;
		}
		#pragma acc loop
		for (int i = 0; i < 10; ++i)
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
			{
			}
		#pragma acc loop
		for (int i = 0; i < 10; ++i)
		{
			for (int j = 0; j < 10; ++j)
			{
				#pragma acc loop
				for (int k = 0; k < 3; ++k)
					oneliner_stmt++;
			}
			#pragma acc loop
			for (int j = 0; j < 10; ++j)
			{
			}
		}
	}
}
