# MLB Draft Data Puller

A personal project: a small command line tool that downloads MLB draft pick data from the MLB Stats API and saves both per year and combined CSV files, so draft history can be analyzed without manual copying. Choose any inclusive year range the API supports. No bundled datasets or API credentials are needed.

## Requirements

Python 3.9 or newer. Install the dependencies in a virtual environment:

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

By default the tool writes `draft_YEAR.csv` for each year and `draft_START_END.csv` for the combined data to `./data/`. Choose another folder with `--output-dir`:

```bash
python pull_mlb_draft.py \
  --start-year 2020 \
  --end-year 2025 \
  --output-dir ./draft-data
```

Each row is one pick and includes the fields the API returns, plus `year` and `pick` columns. Response fields can vary by year, so columns missing in some years are blank in the combined file. The tool reports request or format errors instead of silently producing incomplete output.

## Data source

Data comes from the [MLB Stats API draft endpoint](https://statsapi.mlb.com/api/v1/draft/2025). This is an independent project, not affiliated with or endorsed by Major League Baseball, and use of the data is subject to the source's terms. Generated CSV files are excluded from the repository; run the tool to retrieve your own copy.

## License

No license has been selected yet. Add one before granting others permission to reuse or distribute the code.
