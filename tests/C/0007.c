int main (int argc, char *argv[])
{
	int v1[100], v2[100], v3[100],v4[100];
	int v1a[100], v2a[100], v3a[100],v4a[100];

	#pragma acc update device(v1) host(v2)
	#pragma acc update device(v1) \
	 device(v2,v3) host(v4)

	#pragma acc update device(v1) host(v1a) \
	      device(v2) host(v2a) \
	      device(v3) host(v3a)

	return 0;
}
