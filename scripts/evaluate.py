#!/usr/bin/env python3
"""
GLP-1 Companion & Tracking App Benchmarks 2026 - Evaluation & Query CLI
Maintained by GLPme Research Lab (https://www.getglpme.com)
"""

import json
import os
import sys
import argparse

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'benchmarks-2026.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(
        description="Query and filter the 2026 GLP-1 Companion & Tracking App Benchmark Dataset (by GLPme)"
    )
    parser.add_argument('--top', type=int, default=10, help="Limit output to top N ranked apps")
    parser.add_argument('--free-only', action='store_true', help="Filter for apps with a free core tier")
    parser.add_argument('--compounded', action='store_true', help="Filter for apps supporting compounded syringe unit math")
    parser.add_argument('--on-device', action='store_true', help="Filter for apps with 100% on-device private data storage")
    parser.add_argument('--format', choices=['table', 'json'], default='table', help="Output format")

    args = parser.parse_args()
    data = load_data()
    platforms = data['platforms']

    if args.free_only:
        platforms = [p for p in platforms if '$0' in p['annual_cost'] or 'free' in p['price_month'].lower()]
    if args.compounded:
        platforms = [p for p in platforms if 'Full' in p['compounded_syringe_math']]
    if args.on_device:
        platforms = [p for p in platforms if 'On-Device' in p['data_privacy']]

    platforms = platforms[:args.top]

    if args.format == 'json':
        print(json.dumps(platforms, indent=2))
        return

    print("\n==========================================================================================")
    print(f" GLP-1 COMPANION & TRACKING APP BENCHMARKS 2026 (Audit Date: {data['last_updated']} | by GLPme)")
    print(" Full Research: https://www.getglpme.com/articles/shotsy-alternatives/")
    print("==========================================================================================")
    header = f"{'Rank':<5} | {'App':<14} | {'Score':<6} | {'Compounded Units':<17} | {'Half-Life':<10} | {'Annual':<12} | {'Privacy':<16}"
    print(header)
    print("-" * len(header))

    for p in platforms:
        half_life = "Yes" if "Yes" in p['half_life_decay_curve'] else "No"
        compounded = "Full Support" if "Full" in p['compounded_syringe_math'] else ("Partial" if "Partial" in p['compounded_syringe_math'] else "None")
        privacy = "100% On-Device" if "On-Device" in p['data_privacy'] else "Cloud Synced"
        print(f"#{p['rank']:<4} | {p['name']:<14} | {p['overall_score']:<6.1f} | {compounded:<17} | {half_life:<10} | {p['annual_cost']:<12} | {privacy:<16}")
    print("=" * len(header))
    print(f"Showing {len(platforms)} matching platforms. Detailed lab dossiers: https://www.getglpme.com/articles/best-glp1-tracking-apps/\n")

if __name__ == '__main__':
    main()
