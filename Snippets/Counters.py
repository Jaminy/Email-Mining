import collections

counters = collections.defaultdict(collections.Counter)
counters[email['From']] += 1
counters[email['From']] [date.hour]+= 1
