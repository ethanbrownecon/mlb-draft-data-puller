# MLB Draft Data Puller

A small command-line tool that downloads MLB draft pick data from the MLB Stats
API and saves both per-year and combined CSV files. Choose any inclusive year
range supported by the API; no bundled datasets or API credentials are needed.

## Requirements

- Python 3.9 or newer

Install the dependencies in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Download a range of draft years:

```bash
python pull_mlb_draft.py --start-year 2016 --end-year 2025
```

By default, the tool writes `draft_YEAR.csv` for each year and
`draft_START_END.csv` for the combined data to `./data/`. Choose another output
directory with `--output-dir`:

```bash
python pull_mlb_draft.py \
  --start-year 2020 \
  --end-year 2025 \
  --output-dir ./draft-data
```

Each row represents a pick and includes the response fields returned by the
API, along with `year` and `pick` columns. The API response can vary by year,
so columns that are not present in every year are blank in the combined CSV.
The tool reports request or response-format errors rather than silently
producing incomplete output.

## Data source

Data is requested from the
[MLB Stats API draft endpoint](https://statsapi.mlb.com/api/v1/draft/2025).
This is an independent project and is not affiliated with or endorsed by Major
League Baseball. Data availability and use are subject to the source's terms.
Generated CSV files are excluded from this repository; run the tool to retrieve
your own copy.

## License

No license has been selected for this project yet. Add one before granting
others permission to reuse or distribute the source code.
