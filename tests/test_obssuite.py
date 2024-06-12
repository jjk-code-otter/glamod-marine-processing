from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
from cdm_reader_mapper.cdm_mapper import read_tables
from cdm_reader_mapper.common.getting_files import load_file

from glamod_marine_processing.utilities import mkdir

table_names = [
    "header",
    "observations-at",
    "observations-dpt",
    "observations-slp",
    "observations-sst",
    "observations-wbt",
    "observations-wd",
    "observations-ws",
]

table_names_1b = [
    "header",
    "observations-at",
    "observations-dpt",
    "observations-slp",
    "observations-sst",
    "observations-wd",
    "observations-ws",
]


def _load_NOC_corrections(**kwargs):
    for sub in [
        "duplicate_flags",
        "duplicates",
        "id",
        "latitude",
        "longitude",
        "timestamp",
    ]:
        load_file(
            f"NOC_corrections/v1x2023/{sub}/2022-01.txt.gz",
            **kwargs,
        )


def _load_NOC_ANC_INFO(**kwargs):
    load_file(
        "NOC_ANC_INFO/json_files/dck992.json",
        **kwargs,
    )


def _load_Pub47(**kwargs):
    load_file(
        "Pub47/monthly/2022-01-01.csv",
        **kwargs,
    )


def _load_metoffice_qc(**kwargs):
    for qc_file in [
        "AT_qc_202201_CCIrun.csv",
        "DPT_qc_202201_CCIrun.csv",
        "POS_qc_202201_CCIrun.csv",
        "SLP_qc_202201_CCIrun.csv",
        "SST_qc_202201_CCIrun.csv",
        "SST_qc_202201_hires_CCIrun.csv",
        "Variables_202201_CCIrun.csv",
        "W_qc_202201_CCIrun.csv",
    ]:
        load_file(f"metoffice_qc/base/2022/01/{qc_file}", **kwargs)


def test_level1a(capsys):
    """Testing level1a."""
    load_file(
        "imma1_992/input/114-992_2022-01-01_subset.imma",
        cache_dir="./T1A/datasets/ICOADS_R3.0.2T/level0/114-992",
        within_drs=False,
    )

    s = (
        "obs_suite "
        "-l level1a "
        "-data_dir ./T1A "
        "-work_dir ./T1A "
        "-sp ???-???_????-??-??_subset.imma "
        "-o "
        "-run"
    )
    os.system(s)
    captured = capsys.readouterr()
    assert captured.out == ""

    results = read_tables("./T1A/release_7.0/ICOADS_R3.0.2T/level1a/114-992")
    for table_name in table_names:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./E1A/ICOADS_R3.0.2T/level1a/114-992",
            within_drs=False,
        )
    expected = read_tables("./E1A/ICOADS_R3.0.2T/level1a/114-992")

    del results[("header", "record_timestamp")]
    del expected[("header", "record_timestamp")]
    del results[("header", "history")]
    del expected[("header", "history")]

    pd.testing.assert_frame_equal(results, expected)


def test_level1b(capsys):
    """Testing level1b."""
    _load_NOC_corrections(
        cache_dir="./T1B/release_7.0",
        branch="marine_processing_testing",
    )
    for table_name in table_names:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./T1B/release_7.0/ICOADS_R3.0.2T/level1a/114-992",
            within_drs=False,
        )
    s = (
        "obs_suite "
        "-l level1b "
        "-data_dir ./T1B "
        "-work_dir ./T1B "
        "-sp header-???-???_????-??-??_subset.psv "
        "-o "
        "-run"
    )
    os.system(s)
    captured = capsys.readouterr()
    assert captured.out == ""

    results = read_tables(
        "./T1B/release_7.0/ICOADS_R3.0.2T/level1b/114-992", cdm_subset=table_names_1b
    )

    for table_name in table_names_1b:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./E1B/ICOADS_R3.0.2T/level1b/114-992",
            within_drs=False,
        )
    expected = read_tables(
        "./E1B/ICOADS_R3.0.2T/level1b/114-992", cdm_subset=table_names_1b
    )

    del results[("header", "record_timestamp")]
    del expected[("header", "record_timestamp")]
    del results[("header", "history")]
    del expected[("header", "history")]

    pd.testing.assert_frame_equal(results, expected)


def test_level1c(capsys):
    """Testing level1c."""
    _load_NOC_ANC_INFO(
        cache_dir="./T1C/release_7.0",
        branch="marine_processing_testing",
    )
    for table_name in table_names:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./T1C/release_7.0/ICOADS_R3.0.2T/level1b/114-992",
            within_drs=False,
        )

    s = (
        "obs_suite "
        "-l level1c "
        "-data_dir ./T1C "
        "-work_dir ./T1C "
        "-sp header-???-???_????-??-??_subset.psv "
        "-o "
        "-run"
    )
    os.system(s)
    captured = capsys.readouterr()
    assert captured.out == ""

    results = read_tables(
        "./T1C/release_7.0/ICOADS_R3.0.2T/level1c/114-992", cdm_subset=["header"]
    )
    for table_name in table_names_1b:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./E1C/ICOADS_R3.0.2T/level1c/114-992",
            within_drs=False,
        )
    expected = read_tables(
        "./E1C/ICOADS_R3.0.2T/level1c/114-992", cdm_subset=["header"]
    )

    del results["record_timestamp"]
    del expected["record_timestamp"]
    del results["history"]
    del expected["history"]

    pd.testing.assert_frame_equal(results, expected)


def test_level1d(capsys):
    """Testing level1d."""
    _load_Pub47(
        cache_dir="./T1D/release_7.0",
        branch="marine_processing_testing",
    )
    for table_name in table_names:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./T1D/release_7.0/ICOADS_R3.0.2T/level1c/114-992",
            within_drs=False,
        )

    s = (
        "obs_suite "
        "-l level1d "
        "-data_dir ./T1D "
        "-work_dir ./T1D "
        "-sp header-???-???_????-??-??_subset.psv "
        "-o "
        "-run"
    )
    os.system(s)
    captured = capsys.readouterr()
    assert captured.out == ""

    results = read_tables(
        "./T1D/release_7.0/ICOADS_R3.0.2T/level1d/114-992", cdm_subset=table_names_1b
    )
    for table_name in table_names_1b:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./E1D/ICOADS_R3.0.2T/level1d/114-992",
            within_drs=False,
        )
    expected = read_tables(
        "./E1D/ICOADS_R3.0.2T/level1d/114-992", cdm_subset=table_names_1b
    )

    del results[("header", "record_timestamp")]
    del expected[("header", "record_timestamp")]
    del results[("header", "history")]
    del expected[("header", "history")]

    expected[("header", "station_name")] = [
        "null",
        "FF HELMER HANSEN",
        "WAVERIDER TFSTD",
        "NORNE",
        "WAVERIDER TFDRN",
    ]
    expected[("header", "platform_sub_type")] = ["null", "RV", "OT", "MI", "OT"]
    expected[("header", "station_record_number")] = ["1", "1", "0", "13", "0"]
    expected[("header", "report_duration")] = ["11", "HLY", "11", "HLY", "11"]
    expected[("observations-at", "sensor_id")] = ["null", "AT", np.nan, "null", np.nan]
    expected[("observations-dpt", "sensor_id")] = [
        np.nan,
        "HUM",
        np.nan,
        "null",
        np.nan,
    ]
    expected[("observations-slp", "sensor_id")] = [
        "null",
        "SLP",
        np.nan,
        "null",
        np.nan,
    ]
    expected[("observations-sst", "sensor_id")] = [
        "null",
        "SST",
        np.nan,
        np.nan,
        np.nan,
    ]
    expected[("observations-wd", "sensor_id")] = [
        "null",
        "WSPD",
        np.nan,
        "null",
        np.nan,
    ]
    expected[("observations-ws", "sensor_id")] = [
        "null",
        "WSPD",
        np.nan,
        "null",
        np.nan,
    ]
    expected[("observations-at", "sensor_automation_status")] = [
        "5",
        "3",
        np.nan,
        "5",
        np.nan,
    ]
    expected[("observations-dpt", "sensor_automation_status")] = [
        np.nan,
        "3",
        np.nan,
        "5",
        np.nan,
    ]
    expected[("observations-slp", "sensor_automation_status")] = [
        "5",
        "3",
        np.nan,
        "5",
        np.nan,
    ]
    expected[("observations-sst", "sensor_automation_status")] = [
        "5",
        "3",
        np.nan,
        np.nan,
        np.nan,
    ]
    expected[("observations-wd", "sensor_automation_status")] = [
        "5",
        "3",
        np.nan,
        "5",
        np.nan,
    ]
    expected[("observations-ws", "sensor_automation_status")] = [
        "5",
        "3",
        np.nan,
        "5",
        np.nan,
    ]

    pd.testing.assert_frame_equal(results, expected)


def test_level1e(capsys):
    """Testing level1e."""
    _load_metoffice_qc(
        cache_dir="./T1E/release_7.0",
        branch="marine_processing_testing",
    )
    for table_name in table_names:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./T1E/release_7.0/ICOADS_R3.0.2T/level1d/114-992",
            within_drs=False,
        )

    s = (
        "obs_suite "
        "-l level1e "
        "-data_dir ./T1E "
        "-work_dir ./T1E "
        "-sp header-???-???_????-??-??_subset.psv "
        "-o "
        "-run"
    )
    os.system(s)
    captured = capsys.readouterr()
    assert captured.out == ""

    results = read_tables(
        "./T1E/release_7.0/ICOADS_R3.0.2T/level1e/114-992", cdm_subset=table_names_1b
    )
    for table_name in table_names_1b:
        load_file(
            f"imma1_992/cdm_tables/{table_name}-114-992_2022-01-01_subset.psv",
            cache_dir="./E1E/ICOADS_R3.0.2T/level1e/114-992",
            within_drs=False,
        )
    expected = read_tables(
        "./E1E/ICOADS_R3.0.2T/level1e/114-992", cdm_subset=table_names_1b
    )

    del results[("header", "record_timestamp")]
    del expected[("header", "record_timestamp")]
    del results[("header", "history")]
    del expected[("header", "history")]

    expected[("header", "report_quality")] = ["2", "2", "2", "2", "2"]

    pd.testing.assert_frame_equal(results, expected)


def test_level2():
    """Testing level2."""
