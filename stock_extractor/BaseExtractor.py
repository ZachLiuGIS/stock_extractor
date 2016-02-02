import requests
import time


class BaseExtractor(object):
    class SettingError(Exception):
        pass

    def __init__(self):
        """used to store extract result"""
        self.df = None

    def _get_url_response(self, url, qs):
        success = False
        retry_count = 0
        resp = None

        # try three more times with 5, 25, 125 seconds interval if requests error
        while not success:
            try:
                resp = requests.get(url, qs)
                success = True
            except (requests.HTTPError, requests.ConnectionError) as ex:
                if retry_count < 3:
                    retry_count += 1
                    sleep_period = 5 ** retry_count
                    time.sleep(sleep_period)
                else:
                    raise
        return resp

    def get_dataframe(self):
        """return the dataframe at current state"""
        return self.df

    def save_to_csv(self, filepath='output.csv'):
        """save dataframe to csv"""
        if not filepath[-4:] == '.csv':
            filepath += '.csv'
        self.df.to_csv(filepath, index=True)
