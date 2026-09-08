from src.gpu_log_analyzer import analyze_log_text, extract_level, analyze_log_file, format_summary, main, exit_code_for_counts, format_json_summary, write_report, count_levels
import pytest
import json


def test_known_levels():
    text = "Error : GPU fallenoff the bus\n \
    INfo  : ECC is off\n \
    warning : GPU temperature is high\n "
    assert analyze_log_text(text) == {"ERROR" : 1, "WARNING" : 1, "INFO" : 1}


def test_without_colon_in_line():
    line = "Error"
    assert extract_level(line) == "UNKNOWN"


def test_mixed_levels():
    text = "Error : GPU fallenoff the bus\n \
    INfo  : ECC is off\n \
    warning : GPU temperature is high\n \
    Debug : diagnostic detail, warning : encoder utilization is high \n \
    eRROR: GPU Initialization failed \n \
    WarninG ::GPU utilization is High:80%, error : GPU fallenoff the bus "
    assert analyze_log_text(text) == {"ERROR" : 2, "WARNING" : 2, "INFO" : 1}


def test_empty_text():
    text = " "
    assert analyze_log_text(text) == {"ERROR" : 0, "WARNING" : 0, "INFO" : 0}


def test_analyze_log_file(tmp_path):
    path = tmp_path / "example.txt"
    text = "Error : GPU fallenoff the bus\n \
        INfo  : ECC is off\n \
        warning : GPU temperature is high\n "
    path.write_text(text, encoding="utf-8")
    assert analyze_log_file(path) == {"ERROR" : 1, "WARNING" : 1, "INFO" : 1}


def test_analyze_missing_file(tmp_path):
    path = tmp_path / "example.txt"
    with pytest.raises(FileNotFoundError):
        analyze_log_file(path)


#Mission 09
def test_format_summary_mixed():
    summary = {"INFO" : 3, "WARNING" : 1, "ERROR" : 4}
    assert format_summary(summary) == "ERROR: 4\nWARNING: 1\nINFO: 3"

def test_format_summary_zero():
    summary = {"WARNING" : 0, "INFO" : 0, "ERROR" : 0}
    assert format_summary(summary) == "ERROR: 0\nWARNING: 0\nINFO: 0"

def test_main(tmp_path,capsys):
    path = tmp_path / "example.txt"
    path.write_text("INFO: ecc is off \n WARNING: GPU utilization is high\n ERROR: GPU fallen off the bus", encoding= 'utf-8')
    exit_code = main([str(path)])
    captured = capsys.readouterr()
    assert captured.out ==  "ERROR: 1\nWARNING: 1\nINFO: 1\n"
    assert exit_code == 1 # edited in mission 13

#Mission 13
def test_exit_code_for_counts_all_zero():
    counts = {"INFO" : 0, "WARNING" : 0, "ERROR" : 0}
    assert exit_code_for_counts(counts) == 0

def test_exit_code_for_counts():
    counts = {"INFO" : 3, "WARNING" : 1, "ERROR" : 4}
    assert exit_code_for_counts(counts) == 1


def test_main_no_error(tmp_path,capsys):
    path = tmp_path / "example.txt"
    path.write_text("INFO: ecc is off \n WARNING: GPU utilization is high", encoding= 'utf-8')
    exit_code = main([str(path)])
    captured = capsys.readouterr()
    assert captured.out ==  "ERROR: 0\nWARNING: 1\nINFO: 1\n"
    assert exit_code == 0 # edited in mission 13

#Mission14

def test_format_json_summary():
    counts = {"INFO" : 3, "WARNING" : 1, "ERROR" : 4}
    assert counts == json.loads(format_json_summary(counts))

def test_main_json_summary(tmp_path, capsys):
    path = tmp_path / "example.txt"
    path.write_text("INFO: ecc is off \n WARNING: GPU utilization is high \n ERROR: The GPU is fallen off the bus", encoding= 'utf-8')
    exit_code = main([str(path), "--json"])
    captured = capsys.readouterr()
    assert json.loads(captured.out) == {'ERROR': 1, 'WARNING': 1, 'INFO': 1}
    assert exit_code == 1

#Mission 17

def test_main_missing_log_file(tmp_path, capsys):
    path = tmp_path / "example.txt"
    exit_code = main([str(path)])
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "ERROR: log file not found: " + str(path) + "\n"
    assert exit_code == 2


#Mission 19
def test_write_report(tmp_path):
    path = tmp_path / "report.txt"
    write_report(path, "ERROR: 1")
    assert path.read_text(encoding = 'utf-8') == "ERROR: 1\n"

def test_output_file(tmp_path, capsys):
    logfile_path = tmp_path / "logfile.txt"
    logfile_path.write_text("INFO: ecc is off \n WARNING: GPU utilization is high \n ERROR: The GPU is fallen off the bus", encoding= 'utf-8')
    report_path = tmp_path / "report.txt"
    exit_code = main([str(logfile_path), "--output", str(report_path)])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert report_path.read_text(encoding = 'utf-8') == "ERROR: 1\nWARNING: 1\nINFO: 1\n"


def test_json_output_file(tmp_path, capsys):
    logfile_path = tmp_path / "logfile.txt"
    logfile_path.write_text("INFO: ecc is off \n WARNING: GPU utilization is high \n ERROR: The GPU is fallen off the bus", encoding= 'utf-8')
    report_path = tmp_path / "report.json"
    exit_code = main([str(logfile_path), "--json", "--output", str(report_path)])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert json.loads(report_path.read_text(encoding = 'utf-8')) == {'ERROR' : 1, 'WARNING' :  1, 'INFO' : 1}


def test_count_levels_accepts_raw_levels():
    levels = [ " eRRor ", "WARNING", "  warning", "info  ", " Info  ", "Debug "]
    result = count_levels(levels)
    assert result == {"ERROR": 1, "WARNING": 2, "INFO": 2}


def test_count_levels_does_not_modify_input():
    levels = [ " eRRor ", "WARNING", "  warning", "info  ", " Info  ", "Debug "]
    original_levels = levels.copy()
    count_levels(levels)
    assert levels == original_levels





