int main (int argc, char *argv[])
{
	unsigned N = 100, M = 200, O = 300;
	double super_long_variable_name[N][M][O];
	float ultra_long_variable_name_but_this_is_too_long[M];
	unsigned short_var, shorter, x,y,z,v;
	float and_another_insanely_long_variable_name_used_here[N];

	#pragma acc enter data copyin(super_long_variable_name[1:N][1:M][1:O]) \
	  copyin(short_var) copyin(x,y,z,v) \
	 copyin(and_another_insanely_long_variable_name_used_here[N])

	#pragma acc exit data \
	  copyout(ultra_long_variable_name_but_this_is_too_long[N:M],shorter) \
	  copyout(and_another_insanely_long_variable_name_used_here[N])
}
