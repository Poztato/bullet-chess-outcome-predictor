# Local extension prototypes

- `final_pipeline.py`: fetches the latest available monthly Chess.com archive and computes statistics for the latest completed session. Requires `requests`. It has no browser integration, live move evaluation, or model inference.
- `convert_model.py`: historical attempt to export the random forest as JSON. Its file paths refer to a missing sibling `Chess Scraper` project. It casts tree values to integers and rounds thresholds, so it must be repaired and checked against scikit-learn before use.

Both are retained exactly as found. The [phase two plan](../../docs/phase-2-plan.md) describes the intended replacement work.
