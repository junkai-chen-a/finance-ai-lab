"""Turn quarterly financial data into a traceable earnings brief."""

import argparse
import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path


FIELDS = ('revenue', 'operating_income', 'operating_cash_flow', 'capex')
SAMPLE = Path(__file__).with_name('sample_quarters.csv')


def load_quarters(path):
    quarters = {}
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        if not {'quarter', *FIELDS}.issubset(reader.fieldnames or []):
            raise ValueError('Expected columns: quarter, ' + ', '.join(FIELDS))
        for line, row in enumerate(reader, start=2):
            quarter = row['quarter'] or ''
            if not re.fullmatch(r'[0-9]{4}-Q[1-4]', quarter) or quarter in quarters:
                raise ValueError(f'Line {line}: invalid or duplicate quarter.')
            try:
                values = {field: Decimal(row[field] or '') for field in FIELDS}
            except InvalidOperation as error:
                raise ValueError(f'Line {line}: expected numeric values.') from error
            if not all(value.is_finite() for value in values.values()):
                raise ValueError(f'Line {line}: expected finite values.')
            if values['revenue'] <= 0 or values['capex'] < 0:
                raise ValueError(f'Line {line}: revenue must be positive and capex nonnegative.')
            quarters[quarter] = values
    if not quarters:
        raise ValueError('The CSV contains no quarters.')
    return quarters


def build_brief(quarters):
    latest = max(quarters)
    prior = f'{int(latest[:4]) - 1:04d}{latest[4:]}'
    current = quarters[latest]
    margin = current['operating_income'] / current['revenue']
    fcf = current['operating_cash_flow'] - current['capex']
    lines = [
        f'# {latest} Earnings Brief',
        '',
        f"- Revenue: {current['revenue']:,.2f}",
        f'- Operating margin: {margin:.1%}',
        f'- Free cash flow: {fcf:,.2f}',
    ]
    if prior in quarters:
        previous = quarters[prior]
        growth = current['revenue'] / previous['revenue'] - 1
        previous_margin = previous['operating_income'] / previous['revenue']
        lines.extend([
            f'- Revenue growth vs. {prior}: {growth:+.1%}',
            f'- Operating margin change vs. {prior}: {(margin - previous_margin) * 100:+.1f} pp',
        ])
    else:
        lines.append(f'- Year-over-year comparison unavailable: no data for {prior}.')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', nargs='?', type=Path, default=SAMPLE)
    parser.add_argument('--ai-prompt', action='store_true', help='Print a prompt for a language model.')
    args = parser.parse_args()
    try:
        brief = build_brief(load_quarters(args.csv))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if args.ai_prompt:
        print('Explain the earnings brief in three bullets. Use only the facts below. '
              'Separate observed results from open questions. Do not infer causes, give '
              'investment recommendations, or invent missing values.\n')
    print(brief)


if __name__ == '__main__':
    main()
