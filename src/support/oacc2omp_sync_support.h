#pragma once

#define OACC2OMP_SYNC_SUPPORT_MAX_LEN (1024*1024)

extern char __oacc2omp_sync_dep_array[OACC2OMP_SYNC_SUPPORT_MAX_LEN];
