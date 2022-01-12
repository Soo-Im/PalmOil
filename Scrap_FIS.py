import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_table_info(i):
    print(i)
    url = 'https://www.atfis.or.kr/basicprice/M002010000/itemView.do?page='+str(i)+'&uniqId=0602000002011446&type=monthly&searchStartDate=1992-01-01&searchEndDate=2022-01-11'
    # html 파싱
    req = requests.get(url)
    urlparse = BeautifulSoup(req.text, 'html.parser')

    # html 내의 table을 df로 보낸다
    table = urlparse.find_all('table', class_='table_view2')
    df = pd.read_html(str(table))[1]

    # date 형식을 올바르게 표시하도록 수정한다
    df['기간(월)'] = (df['기간(월)']+1e-4)*(10**4)
    df['기간(월)'] = pd.to_datetime(df['기간(월)'], format='%Y%m%d')
    df['기간(월)'] = pd.to_datetime(df['기간(월)']).dt.date

    return df

def excel_writer(excel_path, dataframe):
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False)
    writer.close()


total_df = pd.DataFrame()
page_range = range(1, 13)
total_df = total_df.append([get_table_info(i) for i in page_range])

excel_writer("PALMOIL_PRESENT.xlsx", total_df)