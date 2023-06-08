#!/usr/bin/python3
import os
import models
import unittest
from models.state import State
from models.base_model import BaseModel


class TestStateModel(unittest.TestCase):
    """Unittests for testing State class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create(self):
        """Test State model creation"""
        state = State()
        all = models.storage.all()
        self.assertIn('id', state.to_dict(), "Missing id")
        self.assertIn('created_at', state.to_dict(), "Missing created_at")
        self.assertIn('updated_at', state.to_dict(), "Missing updated_at")
        self.assertIn('__class__', state.to_dict(), "Missing __class__")

    def test_unique_ids(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)


class Test_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""


if __name__ == "__main__":
    unittest.main()
