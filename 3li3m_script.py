#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, sys, time, os, getpass

def iter_lines(path):
    encodings = ["utf-8", "latin-1"]
    last_err = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc, errors="ignore") as f:
                for line in f:
                    yield line.rstrip("\r\n")
            return
        except Exception as e:
            last_err = e
    print(f"[!] Failed to open file: {last_err}")
    sys.exit(1)

def human(n):
    return f"{n:,}"

def main():
    p = argparse.ArgumentParser(
        description="Local demo: match password from wordlist (no network)"
    )
    p.add_argument("--wordlist", "-w", required=True, help="Path to wordlist file")
    p.add_argument("--progress-every", type=int, default=500000,
                   help="Print progress every N attempts (default 500,000)")
    args = p.parse_args()

    wl = os.path.abspath(args.wordlist)
    if not os.path.isfile(wl):
        print("[!] Wordlist file not found:", wl)
        sys.exit(1)

    real_pw = getpass.getpass("Enter the real password (hidden): ").strip()
    if not real_pw:
        print("[!] Password cannot be empty.")
        sys.exit(1)

    print("\n== Local Simulation (no network) ==")
    print("Wordlist:", wl, "\n")

    start = time.time()
    tried = 0

    for pw in iter_lines(wl):
        tried += 1
        if pw == real_pw:
            dt = time.time() - start
            print(f"\n[✔] Password found: {pw}")
            print(f"[i] Attempts: {human(tried)} | Time: {dt:.2f} s")
            break
        if tried % args.progress_every == 0:
            dt = time.time() - start
            rate = tried / dt if dt > 0 else 0
            print(f"[..] Attempts: {human(tried)} | Speed: {rate:,.0f} words/s")

    else:
        dt = time.time() - start
        rate = tried / dt if dt > 0 else 0
        print(f"\n[✘] Password not found in file.")
        print(f"[i] Total attempts: {human(tried)} | Time: {dt:.2f}s | Speed: {rate:,.0f}/s")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
