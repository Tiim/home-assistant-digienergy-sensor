import requests
import re


class DigiEnergy:
    def __init__(self, url, username=None, password=None) -> None:

        self.url = url
        self.username = username
        self.password = password

        self.token = self.get_token()

        pass

    def get_token(self):
        if not self.username is None and not self.password is None:
            data = {
                "mg": "0",
                "userlevel": "99",
                "user": self.username,
                "password": self.password,
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            url = self.url + "/config/index.htm"
            html = requests.post(url, headers=headers, cookies={}, data=data).text
            matcher = re.search("mg=(-?\d+)&ac", html)
            return matcher.group(1)
        else:
            return None

    """
  http://file.comasys.ch:8080/config/a.dwh?V=%23%23000[20]&mg=-811696201
  """

    def get_sensor_value(self, sensors=[]):

        data = self.load_data(sensors)

        if "§§§" in data:
            self.token = self.get_token()
            data = self.load_data(sensors)

        values = data.split("\n")[: len(sensors)]

        result = []
        for v in values:
            v = int(v.strip()) / 1000
            result.append(v)
        return result

    def load_data(self, sensors):
        params = {"V": sensors}
        if not self.token is None:
            params["mg"] = self.token
        return requests.get(self.url + "/config/a.dwh", params=params).text


def main():
    digi = DigiEnergy(
        "http://file.comasys.ch:8080", username="Service", password="Service"
    )
    values = digi.get_sensor_value(["##000[20]", "##000[17]"])
    print(values)


if __name__ == "__main__":
    main()
