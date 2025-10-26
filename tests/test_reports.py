import pandas as pd

from src.reports import convert_log_to_excel, save_report, spending_by_category


def test_spending_by_category(sample_df):
    result = spending_by_category(sample_df, "Супермаркеты", "2024-12-01", save_to_file=False)
    assert isinstance(result, list)
    for row in result:
        assert "date" in row and "amount" in row and "description" in row
        assert row["amount"] < 0


def test_save_report_creates_file(tmp_path):
    @save_report(filename=str(tmp_path / "test_report.json"))
    def dummy_report(save_to_file=False):
        _ = save_to_file  # подавляет предупреждение линтера
        return {"example": 1}

    dummy_report(save_to_file=True)
    file_path = tmp_path / "test_report.json"
    assert file_path.exists()

    with open(file_path, encoding="utf-8") as f:
        data = f.read()
        assert '"example": 1' in data


def test_log_file_not_found(capsys, tmp_path):
    missing_log_path = tmp_path / "missing.log"
    output_file = tmp_path / "report.xlsx"

    convert_log_to_excel(str(missing_log_path), str(output_file))
    captured = capsys.readouterr()

    assert "[!] Лог-файл" in captured.out
    assert not output_file.exists()


def test_empty_log_file(capsys, tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")
    output_file = tmp_path / "report.xlsx"

    convert_log_to_excel(str(log_file), str(output_file))
    captured = capsys.readouterr()

    assert "[!] Лог пустой" in captured.out
    assert not output_file.exists()


def test_convert_valid_log_to_excel(tmp_path):
    log_file = tmp_path / "test.log"
    output_file = tmp_path / "report.xlsx"

    log_file.write_text(
        "2025-07-10 10:00:00 - INFO - Отчет сформирован\n"
        "2025-07-10 10:05:00 - ERROR - Ошибка при сохранении файла\n",
        encoding="utf-8",
    )

    convert_log_to_excel(str(log_file), str(output_file))

    assert output_file.exists()

    df = pd.read_excel(output_file)
    assert len(df) == 2
    assert set(df.columns) == {"date", "level", "message"}
    assert df.iloc[0]["level"] == "INFO"
    assert "Отчет" in df.iloc[0]["message"]
