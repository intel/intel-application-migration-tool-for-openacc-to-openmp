int main (int argc, char *argv[])
{
	int v[1000],v1[1000],v2[1000],v3[1000],v4[1000];
	int a = 10, b = 15, c = 20, d = 30, e = 40;
	int condA = 1, condB = 0, condC = 1;

	#pragma acc enter data copyin(v[0:10]) copyin(v2[1:11])

	#pragma acc enter data copyin(v1[a:b],v2[c:d]) \
	 copyin(v3[0:10],v4[1:11])

	#pragma acc enter data copyin(v1[a:b],v2[0:d]) \
	 copyin(v3[0:e]) \
	 copyin(v4[1:1000])

	#pragma acc exit data copyout(v[0:10]) copyout(v2[1:11])

	#pragma acc exit data copyout(v1[a:b],v2[c:d]) \
	 copyout(v3[0:10],v4[1:11])

	#pragma acc exit data copyout(v1[a:b],v2[0:d]) \
	 copyout(v3[0:e]) \
	 copyout(v4[1:1000])

	#pragma acc enter copyin (v1, v2) \
	  create (v3, v4) \
	  if ((condA && condB) \
	      || (condA && condC))
}
