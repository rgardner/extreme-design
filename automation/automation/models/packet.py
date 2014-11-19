import time


class Packet(dict):
    """Dictionary wrapper for packet dictionary."""
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self['created_at'] = time.time()

    def to_csv(self):
        created_at = self['created_at']
        name = self['source_addr_long'].__repr__()  # escape hex in string
        data = [0] * 12

        # Iterate over adc samples. (0 - 3)
        for i in range(3):
            key = "adc-{0}".format(i)
            if key in self['samples'][0]:
                data[i] = self['samples'][0][key]

        # Iterate over dio (1 - 7)
        for i in range(7):
            key = "dio-{0}".format(i)
            if key in self['samples'][0]:
                data[i] = self['samples'][0][key]

        # Add din
        if 'din' in self['samples'][0]:
            data[11] = self['samples'][0]['din']

        return "{0}, {1}, {2}".format(created_at, name, str(data).strip('[]'))
