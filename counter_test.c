/*
 * counter_test.c - CSE v1.9
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
 * Run:    ./counter_test        (a few seconds at -O2, up to about a minute at -O0)
 *
 * Expected output:
 *   step 0: counter value 0 (the model's [Kernel-0], the start of the loop)
 *   flip 1 at step 2147483648: 2147483647 -> -2147483648, non-flip steps since last flip: 2147483647
 *   flip 2 at step 4294967296: -1 -> 0, non-flip steps since last flip: 2147483647
 *   total steps to return to 0: 4294967296
 *   positive values: 2147483647, negative values: 2147483648, sign flips: 2
 *   highest counter value (ticks): 4294967295, reached at step 4294967295
 *
 * What matches the model:
 *   - 2 flips per cycle.
 *   - M non-flip steps between the flips (and from the start to flip 1,
 *     and from flip 2 back to the start).
 *   - 4,294,967,296 steps in the closed loop, flips included.
 *   - highest counter value 4,294,967,295, then back to 0.
 *
 * What differs from the model:
 *   - Signed two's complement has one more value on the negative side than
 *     the positive side: 2^31 negatives, 2^31 - 1 positives plus zero.
 *     The model counts whole positions on each side, so its two sides are
 *     equal; the register's two sides are not.
 *   - The model's two counted reversals (P) are not transitions (Global
 *     definitions: transitions = 2^32 - 2). In the C program every iteration
 *     is a "step", including the two flips, so steps = 2^32.
 *   - The C program's `steps` counts the two flips. The model's TICK is
 *     steps - 1; its highest value is 2^32 - 1, which matches.
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

    /* The model's starting state: [Kernel-0], counter at 0, before any transition. */
    printf("step 0: counter value 0 (the model's [Kernel-0], the start of the loop)\n");

    do {
        prev = x;
        u += 1;                /* one increment; wraps at 2^32 by definition */
        x = (int32_t)u;
        steps++;

        if (u > highest) {
            highest = u;
            highest_step = steps;
        }

        /*
         * `since` counts non-flip steps since the last flip.
         *   - It is set to 0 immediately after a flip is printed.
         *   - On the next iteration (a non-flip), it becomes 1.
         *   - So the value printed at the next flip is the count of
         *     non-flip steps between the two flips, not counting the flips
         *     themselves.
         */
        if ((prev < 0) != (x < 0)) {
            flips++;
            printf("flip %llu at step %llu: %d -> %d, non-flip steps since last flip: %llu\n",
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
