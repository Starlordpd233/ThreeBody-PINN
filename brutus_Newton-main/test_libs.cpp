#include <iostream>
#define MPFR_USE_NO_MACRO
#define MPFR_USE_INTMAX_T
#include <gmp.h>
#include <mpfr.h>
#include "mpreal.h"

using namespace mpfr;

int main() {
    std::cout << "GMP version: " << gmp_version << std::endl;
    std::cout << "MPFR version: " << mpfr_get_version() << std::endl;
    
    mpreal::set_default_prec(128);
    mpreal x = "1.234567890123456789";
    std::cout << "mpreal test: " << x << std::endl;
    std::cout << "Libraries are working correctly!" << std::endl;
    
    return 0;
}
