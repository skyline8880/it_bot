import requests


class Session():
    """
    Class for creating sessions.
    """
    def _check_params(self, params: dict) -> str:
        """
        Check if params passed return as string.
        """
        if params != {}:
            return params["params"]

    def get(
            self,
            url: str,
            param_type: str = "params",
            **params) -> requests.Response:
        """
        Method to get data.
        """
        with requests.Session() as session:
            if param_type == "params":
                params = self._check_params(params=params)
                with session.get(url=url, params=params) as response:
                    if response.headers["Content-Type"] == "text/html":
                        return response
                    return response.json()
            with session.get(url=url, data=params) as response:
                if response.headers["Content-Type"] == "text/html":
                    return response
                return response.json()

    def post(
            self,
            url: str,
            param_type: str = "params",
            **params) -> requests.Response:
        """
        Method to post data.
        """
        with requests.Session() as session:
            if param_type == "params":
                params = self._check_params(params=params)
                with session.post(url=url, params=params) as response:
                    if response.headers["Content-Type"] == "text/html":
                        return response
                    return response.json()
            elif param_type == "json":
                with session.post(url=url, json=params["params"]) as response:
                    if response.headers["Content-Type"] == "text/html":
                        return response
                    return response.json()
            with session.post(url=url, data=params["params"]) as response:
                if response.headers["Content-Type"] == "text/html":
                    return response
                return response.json()
