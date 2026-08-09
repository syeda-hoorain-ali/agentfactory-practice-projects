#!/usr/bin/env python3
"""
measure_beat.py — Concept 13's math, applied to your own loop.

This does NOT measure tokens for you — Concept 13 says to "note roughly
how many tokens a run reads and writes." Get those numbers from the real
source: Claude Code prints usage at the end of an interactive session, and
a Routine's run page shows it too. In OpenCode, `opencode export <id>`
gives the full record including token counts.

Once you have input_tokens and output_tokens for one real beat of your
Project 03 loop, run this to get the same numbers the course's worked
example produces (about $0.20/beat, about $20/month at 5 beats/day for
20 days) — but for YOUR loop's actual cadence and token counts.

Usage:
    python3 measure_beat.py --input-tokens 40000 --output-tokens 6000 \
        --beats-per-day 1 --days-per-month 30

    # override pricing if you're on a different model / current pricing:
    python3 measure_beat.py --input-tokens 40000 --output-tokens 6000 \
        --beats-per-day 1 --days-per-month 30 \
        --input-price-per-million 3 --output-price-per-million 15
"""
import argparse


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-tokens", type=float, required=True,
                    help="tokens read in one beat (maker + checker combined)")
    p.add_argument("--output-tokens", type=float, required=True,
                    help="tokens written in one beat (maker + checker combined)")
    p.add_argument("--beats-per-day", type=float, required=True,
                    help="how many times the loop fires per day")
    p.add_argument("--days-per-month", type=float, default=30,
                    help="days per month the loop runs (default 30; use ~20 for weekdays-only)")
    p.add_argument("--input-price-per-million", type=float, default=3.0,
                    help="$ per million input tokens (default 3, standard Sonnet price)")
    p.add_argument("--output-price-per-million", type=float, default=15.0,
                    help="$ per million output tokens (default 15, standard Sonnet price)")
    args = p.parse_args()

    cost_per_beat = (
        (args.input_tokens / 1_000_000) * args.input_price_per_million
        + (args.output_tokens / 1_000_000) * args.output_price_per_million
    )
    beats_per_month = args.beats_per_day * args.days_per_month
    monthly_cost = cost_per_beat * beats_per_month

    print(f"Tokens per beat:    {int(args.input_tokens):,} in / {int(args.output_tokens):,} out")
    print(f"Price:              ${args.input_price_per_million}/M in, "
          f"${args.output_price_per_million}/M out")
    print(f"Cost per beat:      ${cost_per_beat:.4f}")
    print(f"Cadence:            {args.beats_per_day} beat(s)/day x "
          f"{int(args.days_per_month)} days = {int(beats_per_month)} beats/month")
    print(f"Monthly cost:       ${monthly_cost:.2f}")

    if args.beats_per_day > 288:  # more than one beat every 5 minutes (24h * 60 / 5)
        print("\nNote: this cadence fires more than once every 5 minutes.")
        print("Concept 13's warning: frequency, not the command, is what drives cost up.")


if __name__ == "__main__":
    main()
