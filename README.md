# Finance AI Lab

Turn quarterly financial data into a short earnings brief. Python calculates the figures first. The same figures can then be passed to a language model to draft a plain-English summary.

## Run the demo

Use Python 3.9 or newer. The script runs with the standard library.

```bash
python3 analyze.py
python3 analyze.py --ai-prompt
python3 analyze.py path/to/quarters.csv
```

`--ai-prompt` prints a prompt to paste into a model of your choice. The command runs entirely locally.

## Sample result

The included CSV represents a fictional business. All amounts use the same arbitrary unit.

- Q4 2025 revenue was **168.00**, up **20.0%** year over year.
- Operating margin was **14.3%**, down **1.4 percentage points** year over year.
- Free cash flow was **22.00**.

Use `YYYY-Q1` through `YYYY-Q4` for quarter labels, with one row per quarter. Enter revenue, operating income, operating cash flow, and capital expenditure in consistent units. Record capital expenditure as a positive outflow. Free cash flow is operating cash flow minus capital expenditure. Year-over-year comparisons use the same quarter of the previous year when data is available.
