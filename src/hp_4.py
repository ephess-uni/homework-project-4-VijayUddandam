# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    formatted = []
    for date in old_dates:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted.append(date_obj.strftime('%d %b %Y'))
    return formatted



def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    return [start_dt + timedelta(days=i) for i in range(n)]



def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    fees = defaultdict(float)
    patron_ids = set()
    
    with open(infile) as f:
        rows = DictReader(f)
        
        for row in rows:
            patron_ids.add(row['patron_id'])
            
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            return_date = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            
            if return_date > due_date:
                days = (return_date - due_date).days            
                fee = days * 0.25
                fees[row['patron_id']] += fee

    with open(outfile, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=['patron_id','late_fees']) 
        writer.writeheader()
        
        for id in patron_ids:
           writer.writerow({'patron_id': id, 'late_fees': '{0:.2f}'.format(fees.get(id, 0))})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())