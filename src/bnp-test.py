import logging
import sys
import pprint
import collections
import argparse
from enum import Enum
from xml.etree import cElementTree
from xml.etree.ElementTree import Element
from typing import Generator, List, Dict
from dataclasses import dataclass, field
from xml.etree.ElementTree import ParseError


@dataclass
class TradeSummary():
    correlationId: str
    numberOfTrades: int
    state: str
    limit: int
    tradeCounter: int = field(default=0)
    amount: int = field(default=0)

    def __post_init__(self):
        if isinstance(self.numberOfTrades, str):
            try:
                self.numberOfTrades = int(self.numberOfTrades)
            except ValueError as e:
                raise ValueError("error in field numberOfTrades: Error {}"
                                 .format(e))

    class States(Enum):
        REJECTED = 'Rejected'
        ACCEPTED = 'Accepted'
        PENDING = 'Pending'


@dataclass
class Trade():
    correlationId: str
    limit: int
    numberOfTrades: int
    tradeId: str
    amount: int

    def __post_init__(self):
        if isinstance(self.limit, str):
            try:
                self.limit = int(self.limit)
            except ValueError as e:
                raise ValueError("error in field limit. Error {}".format(e))


@dataclass
class GroupSummary():
    results: Dict[str, TradeSummary] = field(default_factory=dict)
    search_key: str = 'Trade'
    duplicates: List[str] = field(default_factory=list)

    def iter_elements(self, filename: str) -> Generator[Element, None, None]:
        try:
            events = cElementTree.iterparse(filename, events=("start", "end"))
            _, root = next(events)
            for event, elem in events:
                if event == "end" and elem.tag == self.search_key:
                    yield elem
                    root.clear()
        except ParseError as e:
            raise(ParseError("unable to parse file [{}]. Error: {}"
                             .format(filename, e)))

    def process_trade(self, trade: Trade) -> None:
        self.results.setdefault(trade.correlationId,
                                TradeSummary(trade.correlationId,
                                             trade.numberOfTrades,
                                             TradeSummary.States.PENDING.value,
                                             trade.limit))

        # res = self.results.get(trade.correlationId)
        res = self.results[trade.correlationId]

        if res.state != TradeSummary.States.REJECTED.value:
            res.tradeCounter += 1
            res.amount += trade.amount

        if res.tradeCounter == res.numberOfTrades:
            res.state = TradeSummary.States.ACCEPTED.value

        # Mark trade as reject when limit OR numberOfTrades are exceeded
        if res.amount > res.limit or \
                res.tradeCounter > res.numberOfTrades:
            res.state = TradeSummary.States.REJECTED.value

    def iter_trades(self, filename: str) -> Generator[Trade, None, None]:

        for _trade in self.iter_elements(filename):
            yield(
                Trade(
                    _trade.get('CorrelationId'),
                    _trade.get('Limit'),
                    _trade.get('NumberOfTrades'),
                    _trade.get('TradeID'),
                    int(_trade.text)
                )
            )

    def process_file(self, filename: str) -> Dict[str, TradeSummary]:
        trades: Generator[Trade, None, None] = self.iter_trades(filename)

        # seen = []
        seen = {}
        for trade in trades:
            # skip duplicate tradeId's
            if trade.tradeId not in seen:
                self.process_trade(trade)
                seen.setdefault(trade.tradeId, True)
            else:
                self.duplicates.append(trade.tradeId)
        return self.results

    def write_file(self, output_file: str, data: Dict[str, Trade]) -> None:
        try:
            with open(output_file, 'w') as f:
                for correlationId in \
                        collections.OrderedDict(sorted(data.items())):
                    trade_summary = data.get(correlationId)
                    f.write('{}, {}, {}\n'.format(trade_summary.correlationId,
                                                  trade_summary.numberOfTrades,
                                                  trade_summary.state))
                f.close()
        except (OSError, IOError) as e:
            raise(IOError("unable to write to file [{}]. Error: {}"
                          .format(outputfile, e)))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('server.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    parser = argparse.ArgumentParser(description='produce summarised trade ' +
                                     'table in results.csv from an xml ' +
                                     'input file (see input.xml)')
    parser.add_argument('file', metavar='f', type=str,
                        help='an xml file to process')
    args = parser.parse_args()

    err: int = 0
    try:
        filename = args.file
        outputfile = 'results.csv'
        logger.info('* starting - inputfile: {}'.format(filename))

        table = GroupSummary()
        results = table.process_file(filename)
        logger.info('writing output file: {}'.format(outputfile))
        table.write_file(outputfile, results)
        # pprint.pprint(results)

    except IndexError as e:
        logger.error('please supply a file')
        err += 1
    except FileNotFoundError as e:
        logger.error('file: {} not found'.format(filename))
        err += 1
    except Exception as e:
        logger.error('runtime error: {}'.format(e))
        err += 1
    logger.info('* exiting - errors={}'.format(err))
    exit(err)
