# DB Delay Risk

**How likely is a Deutsche Bahn train to depart late from a given station, and does machine learning add anything over a simple lookup of past late rates?**

An end-to-end data analysis project in Python. It estimates the probability that a scheduled stop departs at least 6 minutes late, tests that estimate on a month no method has seen, and lets the evidence decide whether machine learning is worth its extra complexity.

**Status:** milestones 1 and 2 of 6 done; milestone 4 (baselines) is next. See [Project status](#project-status).

## The question

A traveller with a 7-minute connection does not need the average delay of German trains. What matters is how risky *this* train is, at *this* station, at *this* time.

> Given a scheduled stop (a train service, a station, a scheduled time), what is the probability that the train departs at least 6 minutes late?

Cancellations are a different risk from lateness, so they get their own number: the probability that a scheduled departure is cancelled. The late probability is then for trains that do run.

## Headline result

> **Not measured yet.** This section holds the September results: how much better the chosen method is than a naive guess, and whether machine learning was worth it.

## Approach

Starting with the simplest method that could work, and moving to a more complex one only when the evidence shows the simple one is not good enough.

| Step | Method | Plain-words meaning |
|---|---|---|
| 1 | Overall late rate | One number for every train (the naive guess) |
| 2 | Group rates | Late rate per train type, station or hour |
| 3 | Lookup table with fallback | The history of this exact service at this station, falling back to a broader group when there are too few past stops |
| 4 | Machine learning model | Used only if it clearly beats step 3 and stays honest |

**Success metric.** The Brier score: the average of (predicted probability minus what actually happened) squared, where late is 1 and on time is 0. Lower is better, and confident wrong predictions are punished hard. Log loss is reported alongside it. A method has to beat the naive guess, and its probabilities have to be calibrated (when it says 30%, about 30% of those trains are late), checked with a 10-bin calibration table.

**When machine learning wins.** Fixed before any September score exists. Machine learning replaces the lookup only if, on September, all three hold:

1. Its Brier score is at least about 5% lower than the lookup chosen on August.
2. It wins on enough September days in a daily sign test (5% significance level).
3. Its calibration gap is no larger than the lookup's.

**Honest testing.** Earlier months are for learning, August is for choosing between methods, and September is scored once, at the end. The split is by time, never random, because a random split leaks the future into the past. Methods are compared day by day, because stops on the same day or the same journey are late together and are not independent evidence.

## What the data checks show (July)

| Check | Finding |
|---|---|
| What the delay column measures | Where a train departs, it is the departure delay in every row checked (13,149,769 of 13,149,769). Where there is no planned departure, it holds the arrival delay instead. |
| Missing delays | All of them sit on stops with no planned departure. |
| Duplicates | 1,255 extra copies of the same stop (about 1 in 10,000). |
| Planned times | 97.4% of stops belong to a service × station pair with a single planned hour across July. |

**Cleaning rules decided** (applied in the next step, every removed row counted and printed):

- Stops with no planned departure are left out, since nobody boards there.
- Buses (train type `Bus`) are left out; `SBH` is kept.
- Extra copies of the same scheduled stop are dropped, keeping the first.
- Extreme delays are kept: about 1 in 10,000 rows, too few to change the results.

## Questions the analysis answers

| Question | Why it matters for the decision |
|---|---|
| What is in the data? | Is there enough to work with? |
| Do some trains, stations or hours run later than others? | If everything is equally late, nothing can be predicted beyond the average |
| Are there enough examples per case? | A rate from 3 examples is unreliable; one from 100 starts to be |
| Does the past repeat? | If one month's patterns do not hold in the next, history cannot predict the future |
| Do factors combine in ways a lookup misses? | This is where machine learning could earn its place |

## Data

- Source: [piebro/deutsche-bahn-data](https://huggingface.co/datasets/piebro/deutsche-bahn-data) on Hugging Face, built from Deutsche Bahn's public timetable data.
- Licence: CC BY 4.0. See the dataset page for the exact attribution terms.
- Files used: six monthly files, `data-2026-04.parquet` to `data-2026-09.parquet`, from `monthly_processed_data/`. Each holds 14.5 to 15.1 million stops.
- The data is not stored in this repository. See [Run it yourself](#run-it-yourself).

## How the work is run

- **Version control:** small commits, each with one purpose and a clear prefix (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
- **Code principles:** KISS, YAGNI, DRY and single-purpose functions, following [webpro/programming-principles](https://github.com/webpro/programming-principles).
- **Reproducibility:** pinned dependencies and no hard-coded paths. Shared settings (folders, months, the 6-minute rule) are defined once in `src/dbdelay/config.py`; each notebook keeps only its own display settings at the top.
- **Notebooks vs code:** the notebooks tell the story; shared logic lives in `src/dbdelay/`.
- **No silent cleaning:** every row that is left out is counted and printed.

## Project status

| Milestone | Deliverable | Status |
|---|---|---|
| 1. Setup | Repository, environment, README, data loading | Done |
| 2. Data checks | What the columns mean, duplicates, cancellations, cleaning rules | Done (rules decided; applied in the next step) |
| 3. Late rate by train type and station | Which train types and stations are late most often | Analysed on July; write-up follows the rerun with the cleaning rules |
| 4. Baselines | Naive guess, group rates, lookup table, scored on September | Next |
| 5. Machine learning decision | Is machine learning needed? Written memo with evidence | Not started |
| 6. Final write-up | Headline result, charts, limitations | Not started |

## Repository structure

```
db-delay-risk/
  README.md
  pyproject.toml     makes src/dbdelay installable
  requirements.txt
  .gitignore
  data/              raw data files, not committed
  notebooks/         01_analysis.ipynb, 02_data_checks.ipynb
  src/dbdelay/       settings, loading, cleaning and scoring code
  reports/figures/   saved charts
  reports/tables/    saved tables
```

## Run it yourself

```
git clone https://github.com/<your-username>/db-delay-risk.git
cd db-delay-risk
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .                 # makes src/dbdelay importable from the notebooks
```

Download the six data files listed above into `data/`, open a notebook in `notebooks/` in VS Code and select the `.venv` kernel.

## Limitations

- The data comes from periodic snapshots of DB's timetable data, so it may not record every train. Coverage has not been measured yet.
- Six months (April to September) cannot show winter effects such as snow and ice.
- The patterns found describe when delays happen, not why they happen.
- Predictions use only schedule information known in advance, not the delay already seen earlier on the same journey.

## Next steps

- A separate live version could use the delay already seen earlier on the same journey. That is a different question from this project's planning-time prediction.
- Check how sensitive the results are to the lateness threshold (3 and 15 minutes).
- Add weather data.
- Add automated tests and a data download script.

## Credits

Data: Deutsche Bahn, via piebro/deutsche-bahn-data (CC BY 4.0). Code licence: to be added.
