import csv
from datetime import date

import pytest

from scripts.vaa_independent_replication import ALL_ASSETS, read_prices, reproduce


def write_csv(path, *, missing_asset=None, latest_date="2026-09-30"):
    fields = ["Date", *ALL_ASSETS]
    start_year, start_month = 2025, 9
    dates = []
    year, month = start_year, start_month
    for _ in range(13):
        # Use calendar month-end dates as a deterministic fixture, not market data.
        from calendar import monthrange
        dates.append(date(year, month, monthrange(year, month)[1]).isoformat())
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    dates[-1] = latest_date
    if missing_asset:
        fields.remove(missing_asset)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for i, observed in enumerate(dates):
            row = {"Date": observed}
            for j, asset in enumerate(ALL_ASSETS):
                row[asset] = str(100 + i * (j + 1) / 10)
            writer.writerow({key: value for key, value in row.items() if key in fields})


def test_independent_oracle_reads_complete_csv_and_reproduces_signal(tmp_path):
    path = tmp_path / "fixture.csv"
    write_csv(path)
    dates, prices = read_prices(path, date(2026, 10, 18))
    report = reproduce(dates, prices)
    assert report["signal_date"] == "2026-09-30"
    assert set(report["scores"]) == set(ALL_ASSETS)
    assert sum(report["weights"]) == pytest.approx(1.0)
    assert len(report["selected_assets"]) == len(set(report["selected_assets"]))
    assert report["evidence_boundary"].startswith("Independent formula oracle only")


def test_independent_oracle_fails_closed_on_missing_asset_column(tmp_path):
    path = tmp_path / "missing.csv"
    write_csv(path, missing_asset="SPY")
    with pytest.raises(ValueError, match="missing required asset columns: SPY"):
        read_prices(path, date(2026, 10, 18))


def test_independent_oracle_rejects_incomplete_month_cutoff(tmp_path):
    path = tmp_path / "stale.csv"
    write_csv(path)
    with pytest.raises(ValueError, match="last completed calendar month"):
        read_prices(path, date(2026, 11, 18))
