import argparse
import json
import logging
import os
import shutil
import sys

import pytest
import inspect
import warnings

from atomsci.ddm.utils import model_file_reader as mfr

from pathlib import Path

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

model_path = '../../examples/BSEP/models/bsep_classif_scaffold_split.tar.gz'
tar_model = mfr.ModelTar(model_path)

def test_model_split_uuid():
    split_uuid = tar_model.get_split_uuid()

    assert split_uuid == '162b11b7-da6a-49bd-b85e-2971a0b0a949'

def test_model_uuid():
    model_uuid = tar_model.get_model_uuid()

    assert model_uuid == 'f12a02d3-9238-48b4-883d-3f3775d227a2'

def test_model_type():
    model_type = tar_model.get_model_type()

    assert model_type == 'NN'


    


