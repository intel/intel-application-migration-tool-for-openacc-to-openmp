int main (int argc, char *argv[])
{
	int v[3], v2[4][5],v3[6][7][8];

	#pragma acc enter data copyin(v[:2])

	#pragma acc enter data copyin(v)

	#pragma acc enter data copyin(v2[:4][:5])

	#pragma acc enter data copyin(v2)

	#pragma acc enter data copyin(v3[:3][:7][:8])

	#pragma acc enter data copyin(v3)

	#pragma acc exit data copyout(v3[:2][:7][:8])

	#pragma acc exit data copyout(v3)

	#pragma acc exit data copyout(v2[:1][:5])

	#pragma acc exit data copyout(v2)

	#pragma acc exit data copyout(v[:3])

	#pragma acc exit data copyout(v)

	return 0;
}
