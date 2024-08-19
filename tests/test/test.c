#include <stdio.h>
#include <stdbool.h>

bool is_prime(long long n)
{
    if (n == 2)
        return true;

    if (n % 2 == 0)
        return false;
    long long d = 3;
    while (d * d <= n)
    {
        if (n % d == 0)
            return false;

        d = d + 2;
    }

    return true;
}

int main()
{
    long long n = 10000000;
    FILE *out_file = fopen("output.txt", "w");

    for (long long it = 0; it < n; it++)
    {
        if (is_prime(it))
            fprintf(out_file, "%lld\n", it);
    }

    return 0;
}