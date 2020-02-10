import pytest
import importlib
from xml.etree.ElementTree import ParseError
bnptest = __import__('bnp-test')


class Test():

    @pytest.fixture
    def _group_summary(self):
        return bnptest.GroupSummary()

    @pytest.fixture
    def _filename(self):
        return './test/fixtures/input.xml'

    @pytest.fixture
    def _bad_filename(self):
        return './foo.xml'

    @pytest.fixture
    def _bad_xml(self):
        return './test/fixtures/bad_xml.xml'

    @pytest.fixture
    def _dup_xml(self):
        return './test/fixtures/duplicate_trade.xml'

    @pytest.fixture
    def _too_many_xml(self):
        return './test/fixtures/too_many_trades.xml'

    def test_01_iterfile(self, _filename, _group_summary):
        assert len(list(_group_summary.iter_elements(_filename))) > 0

    def test_02_iterfile_bad_name(self, _bad_filename, _group_summary):
        try:
            len(list(_group_summary.iter_elements(_bad_filename))) > 0
        except FileNotFoundError:
            return
        raise Exception("filename {} should cause file not found error"
                        .format(_bad_filename))

    def test_03_create_trade_from_elem(self, _filename, _group_summary):
        _trade = list(_group_summary.iter_elements(_filename))[0]
        trade = bnptest.Trade(
            _trade.get('CorrelationId'),
            _trade.get('Limit'),
            _trade.get('NumberOfTrades'),
            _trade.get('TradeId'),
            int(_trade.text)
        )
        assert trade.correlationId == "234"

    def test_04_add_trade_to_summary(self, _filename, _group_summary):
        _trade = list(_group_summary.iter_elements(_filename))[0]
        trade = bnptest.Trade(
            _trade.get('CorrelationId'),
            _trade.get('Limit'),
            _trade.get('NumberOfTrades'),
            _trade.get('TradeId'),
            int(_trade.text)
        )
        _group_summary.process_trade(trade)
        assert len(_group_summary.results.keys()) == 1

    def test_05_aggregation(self, _filename, _group_summary):
        _group_summary.process_file(_filename)
        assert len(_group_summary.results.keys()) == 3

    def test_06_duplicate(self, _dup_xml, _group_summary):
        _group_summary.process_file(_dup_xml)
        assert _group_summary.results.get('234').amount == 500
        assert len(_group_summary.duplicates) == 1

    def test_07_too_many_trades(self, _too_many_xml, _group_summary):
        _group_summary.process_file(_too_many_xml)
        assert _group_summary.results.get('234').state == 'Rejected'

    def test_08_bad_xml(self, _bad_xml, _group_summary):
        try:
            _group_summary.process_file(_bad_xml)
        except ParseError as e:
            return
        raise(e)
