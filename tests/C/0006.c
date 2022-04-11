int main (int argc, char *argv[])
{
	int v1[1000], v2[1000], v3[1000];

	#pragma acc update host(v1)

	#pragma acc update host(v1) \
	 host(v2,v3)

	#pragma acc update host(v1) \
	 host(v2) \
	 host(v3)

	return 0;
}
