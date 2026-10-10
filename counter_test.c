/*
 * counter_test.c - CSE v1.6
 *
 * Runs a real 32-bit counter through one full loop and counts every step
 * and every sign flip. Compare the result with CSE_MODEL.txt:
 *
 *   CYCLE COUNT (Global definitions, Nest 0):
 *     1 + 2,147,483,647 + 1 + 2,147,483,647 = 4,294,967,296
 *   TICK (Global definitions) and Total Runtime (Nest 2, Rules 9 and 10):
 *     highest counter value = 2^32 - 1 = 4,294,967,295, then back to 0
 *   The 32-Bit Register (Nest 12, Rule 5):
 *     2^32 states, and the largest signed value is M = 2,147,483,647
 *
 * Build:  gcc -O2 -o counter_test counter_test.c
 * Run:    ./counter_test        (a few seconds)
 *
 * Expected output:
 *   flip 1 at step 2147483648: 2147483647 -> -2147483648, plain steps since last flip: 2147483647
 *   flip 2 at step 4294967296: -1 -> 0, plain steps since last flip: 2147483647
 *   total steps to return to 0: 4294967296
 *   positive values: 2147483647, negative values: 2147483648, sign flips: 2
 *   highest counter value (ticks): 4294967295, reached at step 4294967295
 *
 * What matches the model:  2 flips per cycle, M plain steps between them,
 *                          4,294,967,296 steps in the closed loop,
 *                          highest counter value 4,294,967,295, then 0.
 * What differs:            in the computer each flip is itself a step, and the
 *                          negative side has one more value than the positive side.
 */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t u = 0;            /* the 32-bit register */
    int32_t x = 0, prev = 0;   /* the same bits, read as a signed value */
    uint64_t steps = 0, flips = 0, since = 0;
    uint64_t pos = 0, neg = 0;
    uint32_t highest = 0;      /* the same bits, read as the runtime counter */
    uint64_t highest_step = 0;

    do {
        prev = x;
        u += 1;                /* one increment; wraps at 2^32 by definition */
        x = (int32_t)u;
        steps++;

        if (u > highest) {
            highest = u;
            highest_step = steps;
        }

        if ((prev < 0) != (x < 0)) {
            flips++;
            printf("flip %llu at step %llu: %d -> %d, plain steps since last flip: %llu\n",
                   (unsigned long long)flips, (unsigned long long)steps, prev, x,
                   (unsigned long long)since);
            since = 0;
        } else {
            since++;
        }

        if (x > 0) pos++;
        else if (x < 0) neg++;
    } while (x != 0);

    printf("total steps to return to 0: %llu\n", (unsigned long long)steps);
    printf("positive values: %llu, negative values: %llu, sign flips: %llu\n",
           (unsigned long long)pos, (unsigned long long)neg, (unsigned long long)flips);
    printf("highest counter value (ticks): %llu, reached at step %llu\n",
           (unsigned long long)highest, (unsigned long long)highest_step);
    return 0;
}
