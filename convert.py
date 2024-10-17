#!/usr/bin/env python3

import re
from dateutil.parser import parse
from beancount.core import data, amount
from beancount.core.number import D

from beancount.ingest import importer

PAYEE_REGEX = re.compile(r"，?(.*)(捐赠|垫付)")

class CashImporter(importer.ImporterProtocol):

    def process_line(self, cols):
        no, _, time_str, src, dst, cur, amt_str, note = cols
        metadata = data.new_metadata('cash.md', no)
        time = parse(time_str)
        date = time.date()
        units = amount.Amount(D(amt_str), cur)
        metadata["time"] = time.time().isoformat()

        if m := PAYEE_REGEX.match(note):
            payee = m.group(1)
        else:
            payee = None

        return data.Transaction(
                        meta=metadata,
                        date=date,
                        payee=payee,
                        flag=self.FLAG,
                        narration=note,
                        tags=set(),
                        links=data.EMPTY_SET,
                        postings=[
                            data.Posting(
                                account=src,
                                units=units,
                                cost=None,
                                price=None,
                                flag=None,
                                meta=None,
                            ),
                            data.Posting(
                                account=dst,
                                units=None,
                                cost=None,
                                price=None,
                                flag=None,
                                meta=None,
                            ),
                        ],
                    )

    def identify(self, file):
        return True
    
    def extract(self, file, existing_entries):
        entries = list(existing_entries or [])
        with open('cash.md') as f:
            lines = f.readlines()

        begin_table = False
        for l in lines:
            l = l.strip()
            if begin_table:
                cols = [c.strip() for c in l.split('|')]
                entries.append(self.process_line(cols))
            elif l.startswith('---'):
                begin_table = True

        return entries


CONFIG = [
    CashImporter()
]
