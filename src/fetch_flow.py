import pandas as pd
import requests

def fetch_usgs_flow(site_no: str, start: str, end: str) -> pd.DataFrame:
    url = (
        "https://waterservices.usgs.gov/nwis/dv?"
        f"format=json&sites={site_no}&startDT={start}&endDT={end}&parameterCd=00060"
    )
    resp = requests.get(url)
    data = resp.json()['value']['timeSeries'][0]['values'][0]['value']
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['dateTime']).dt.date
    df['flow'] = pd.to_numeric(df['value'])
    return df[['date', 'flow']]