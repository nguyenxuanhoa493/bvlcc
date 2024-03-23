import requests, time
import streamlit as st
import pandas as pd
from urllib import parse
import urllib3

urllib3.disable_warnings()


def current_time_ts():
    return "&_=" + str(int(time.time() * 1000))


class Cc:
    def __init__(
        self,
    ) -> None:
        self.api = "https://olt.mof.gov.vn/Portal.IU.API/api/"
        self.payload = {}
        self.headers = {
            "authority": "olt.mof.gov.vn",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "vi,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json; charset=utf-8",
            "cookie": "",
            "referer": "https://olt.mof.gov.vn/Portal.IU.CMS/Default.aspx",
            "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        self.id = "79226B0E4C85415ABDFE9CD719BA0962"

    def change_id(self, new_id):
        if new_id:
            self.id = new_id

    def send(self, url):
        response = requests.request(
            "GET",
            self.api + url + current_time_ts(),
            headers=self.headers,
            data=self.payload,
            verify=False,
        )
        return response.json()

    def GetListSoQuyetDinh(self, key=""):
        url = (
            r"DocumentAcceptNumber/GetListSoQuyetDinhByCom?strTuKhoa="
            + key
            + r"&pageIndex=1&pageSize=10000&iTrangThai=2&FromDate=01%2F01%2F1970&ToDate=12%2F31%2F2030&Companyid="
            + self.id
            + "&User_id=&Managecategory_id="
        )
        response = self.send(url)
        return response["Data"]

    def get_id_contest_by_code(self, code_contest):
        url = (
            r"Course/getListAcc?keyword="
            + code_contest
            + "&companyId="
            + self.id
            + "&companySubId=&provinceId=&fromDate=11%2F02%2F1970&toDate=11%2F07%2F2030&status=8&examType=&pageIndex=1&pageSize=1"
        )
        response = self.send(url)
        try:
            return response["Data"][0]
        except:
            return False

    def get_result_contest(self, id_contest):
        url = r"Staff/getStaffByCourseId?courseId=" + id_contest
        response = self.send(url)
        try:
            return response["Data"]
        except:
            return False

    def get_cc_contest(self, id_contest):
        url = r"Staff/GetStaffCertByCourseId?courseId=" + id_contest
        response = self.send(url)
        try:
            return response["Data"]
        except:
            return False

    def get_company(self):
        url = r"Company/getList?cateId=&strCompanyIdList=&provinceId=&status=1&fromDate=-1&toDate=-1"
        response = self.send(url)
        list_company = {}
        list_company_name = []
        for i in response["Data"]:
            list_company[i["CompanyName"]] = i["Id"]
            list_company_name.append(i["CompanyName"])
        list_company_name = list_company_name
        idx_bvl = list_company_name.index("Tổng Công ty Bảo Việt Nhân thọ")
        return list_company, list_company_name, idx_bvl

    def get_user(self, index_page="1", limit="50", key=""):
        key_encode = parse.quote_plus(key)
        url = (
            r"Staff/getList?status=1&companyId="
            + self.id
            + "&companySubId=&provinceId=&keyword="
            + key_encode
            + "&pageIndex="
            + index_page
            + "&pageSize="
            + limit
        )
        response = self.send(url)

        try:
            data = pd.DataFrame(response["Data"])
            data = data[
                [
                    "CompanyName",
                    "CompanySubName",
                    "UserName",
                    "Password",
                    "FullName",
                    "Email",
                    "Mobile",
                    "AddressName",
                    "SexName",
                    "BirthdayPicker",
                    "CardNumber",
                    "IssueDatePicker",
                    "IssuePlace",
                    "CCCDNumber",
                    "CCCDIssueDatePicker",
                    "CCCDExpiredDate",
                    "CCCDExpiredDatePicker",
                    "CCCDIssuePlace",
                    "TongSoLuotThi",
                    "Tel",
                ]
            ]
            return data
        except:
            return []


st.title("Danh sách tài khoản")
main = Cc()
list_company, list_company_name, idx_bvl = main.get_company()

with st.form(key="my_form"):
    c1, c2, c3, c4, c5 = st.columns([4, 2, 1, 1, 2])
    with c1:
        company_name = st.selectbox(
            "Chọn công ty", list_company_name, index=idx_bvl, key="company_name"
        )

    with c2:
        input_text = st.text_input("Tìm kiếm:")
    with c3:
        page_idx = st.text_input("Trang:", value=1)
    with c4:
        limit = st.text_input("Số lượng tối đa:", value=10)
    with c5:
        st.write("")
        st.write("")
        convert = st.form_submit_button("tìm kiếm")


def showqd():
    global company_name, main, list_company
    main.change_id(list_company[company_name])
    list_user = main.get_user(index_page=page_idx, limit=limit, key=input_text)
    st.dataframe(list_user, hide_index=True, width=2000)


if convert and input_text:
    showqd()

else:
    showqd()
