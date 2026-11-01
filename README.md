# DB Delay Risk

**How likely is a specific Deutsche Bahn train to be late, and do we need machine learning to say so?**

An end-to-end data analysis project in Python. It estimates the probability that a train is late at a given station, scores that estimate honestly on data it has never seen, and uses the evidence to decide whether machine learning is worth using.

**Status:** in progress, Phase 1 of 5. See [Project status](#project-status).

## The question

A traveller with a 7-minute connection does not need to know the average delay of German trains. They need to know how risky *this* train is, at *this* station, at *this* time.

> Given a scheduled stop (a train service, a station, a scheduled time), what is the probability that the train arrives at least 6 minutes late?

## Headline result

> **Pending.** This section will be completed at the end of Phase 4 with measured numbers: how much better the chosen method is than a naive guess on unseen data, and whether machine learning was worth its extra complexity.

## Approach

Start with the simplest method that could work. Move to a more complex one only if the evidence says the simple one is not good enough.

| Step | Method | Plain-words meaning |
|---|---|---|
| 1 | Overall late rate | One number for every train (the naive guess) |
| 2 | Group rates | Late rate per train type, station or hour |
| 3 | Lookup table with fallback | Use the history of this exact service and stop; fall back to a broader group when there are too few examples |
| 4 | Machine learning model | Only if it clearly beats step 3 and stays honest |

**Success metric.** The Brier score: the average of (predicted probability minus what actually happened) squared, where late is 1 and on time is 0. Lower is better, and confident wrong predictions are punished hard. A method must beat the naive guess, and its probabilities must be calibrated (when it says 30%, about 30% of those trains are late).

**Honest testing.** July and August are the history. September is the exam: no method sees it while being built. Splits are by time, never random, because a random split leaks the future into the past.

## Questions the analysis answers

| Question | Why it matters for the decision |
|---|---|
| What is in the data? | Is there enough to work with? |
| Do some trains, stations or hours run later than others? | If everything is equally late, nothing can be predicted beyond the average |
| Are there enough examples per case? | A rate from 3 examples is unreliable; one from 100 starts to be |
| Does the past repeat? | If July patterns do not hold in August, history cannot predict the future |
| Do factors combine in ways a lookup misses? | This is where machine learning could earn its place |

## Data

- Source: [piebro/deutsche-bahn-data](https://huggingface.co/datasets/piebro/deutsche-bahn-data) on Hugging Face, built from Deutsche Bahn's public timetable data.
- Licence: CC BY 4.0. See the dataset page for the exact attribution terms.
- Files used: `data-2026-07.parquet`, `data-2026-08.parquet`, `data-2026-09.parquet` from `monthly_processed_data/`.
- The data is not stored in this repository. See [Run it yourself](#run-it-yourself).

## How the work is run

- **Version control:** small commits with clear messages (`feat:`, `fix:`, `docs:`, `chore:`). After the initial setup, every change goes through a branch and a pull request so it can be reviewed.
- **Code principles:** KISS, YAGNI, DRY and single-purpose functions, following [webpro/programming-principles](https://github.com/webpro/programming-principles).
- **Reproducibility:** pinned dependencies, no hard-coded paths, settings defined once at the top of the notebook.
- **Notebook vs code:** the notebook tells the story. Reusable logic moves into `src/dbdelay/` once it is stable.

## Project status

| Phase | Deliverable | Status |
|---|---|---|
| 1. Setup | Repository, environment, README, data loading | In progress |
| 2. Understand the data | Coverage, cleaning decisions, spread of delays | Not started |
| 3. Baselines | Naive guess, group rates, lookup table, scored on September | Not started |
| 4. Decision | Is machine learning needed? Written memo with evidence | Not started |
| 5. Write-up | Headline result, charts, limitations | Not started |

## Repository structure

```
db-delay-risk/
  README.md
  requirements.txt
  .gitignore
  data/              raw data files, not committed
  notebooks/         01_analysis.ipynb
  src/dbdelay/       reusable functions
  reports/figures/   saved charts
```

## Run it yourself

```
git clone https://github.com/<your-username>/db-delay-risk.git
cd db-delay-risk
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Download the three data files listed above into `data/`, open `notebooks/01_analysis.ipynb` in VS Code and select the `.venv` kernel.

## Limitations

- The data comes from periodic snapshots of DB's timetable data, so it may not record every train. Coverage is measured in Phase 2.
- Three months cannot show seasonal effects such as winter weather.
- Patterns found describe when delays happen, not why they happen.
- Predictions use only schedule information known in advance, not the delay already seen earlier on the same journey.

## Next steps

- Use the delay already observed at the previous stop to sharpen the prediction.
- Check how sensitive the results are to the lateness threshold (3 and 15 minutes).
- Add weather data.
- Add automated tests and a data download script.

## Credits

Data: Deutsche Bahn, via piebro/deutsche-bahn-data (CC BY 4.0). Code licence: to be added.
