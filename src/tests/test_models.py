import unittest
import pytest

from pydantic import ValidationError

from app.models import TranslationDelivered, AggregatedOutput


class TestModel(unittest.TestCase):

    def setUp(self):
        self.test_msg = {
            "timestamp": "2018-12-26 18:12:19.903159",
            "translation_id": "5aa5b2f39f7254a75aa4",
            "source_language": "en",
            "target_language": "fr",
            "client_name": "airliberty",
            "event_name": "translation_delivered",
            "duration": 20,
            "nr_words": 100
        }

    def test_translation_delivered_success(self):
        TranslationDelivered(**self.test_msg)

        self.test_msg["timestamp"] = "2018-12-26"
        TranslationDelivered(**self.test_msg)

        self.test_msg.update({
            "duration": "20",
        })
        TranslationDelivered(**self.test_msg)

    def test_translation_delivered_wrong_ts(self):
        with pytest.raises(ValidationError):
            self.test_msg["timestamp"] = "a_string"
            TranslationDelivered(**self.test_msg)

        with pytest.raises(ValidationError):
            self.test_msg["timestamp"] = ""
            TranslationDelivered(**self.test_msg)

    def test_translation_delivered_missing(self):
        with pytest.raises(ValidationError):
            self.test_msg.pop("duration")
            TranslationDelivered(**self.test_msg)


class TestAggregatedOutput(unittest.TestCase):

    def setUp(self):
        self.test_msg = {
            "date": "2018-12-26 18:11:00",
            "average_delivery_time": 0
        }

    def test_aggregated_output_success(self):
        AggregatedOutput(**self.test_msg)

        self.test_msg["date"] = "2018-12-26"
        AggregatedOutput(**self.test_msg)

        self.test_msg.update({
            "average_delivery_time": "0"
        })
        AggregatedOutput(**self.test_msg)

    def test_aggregated_output_missing(self):
        for i in [
            "date",
            "average_delivery_time"
        ]:
            test = self.test_msg.copy()
            with pytest.raises(ValidationError):
                test.pop(i)
                TranslationDelivered(**test)
