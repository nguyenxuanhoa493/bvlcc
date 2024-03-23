import requests, time
import streamlit as st
import pandas as pd
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
            r"/DocumentAcceptNumber/GetListSoQuyetDinhByCom?strTuKhoa="
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


st.set_page_config(page_title="Danh sách quyết định và kết quả thi", layout="wide")
st.title("Danh sách quyết định và kết quả thi")

main = Cc()
list_company, list_company_name, idx_bvl = main.get_company()

with st.form(key="my_form"):
    c1, c2, c3 = st.columns([5, 3, 2])
    with c1:
        company_name = st.selectbox(
            "Chọn công ty", list_company_name, index=idx_bvl, key="company_name"
        )

    with c2:
        input_text = st.text_input("Mã quyết định:")
    with c3:
        st.write("")
        st.write("")
        convert = st.form_submit_button("tìm kiếm")


def showqd(input_text):
    global company_name, main, list_company
    main.change_id(list_company[company_name])
    list_qd = main.GetListSoQuyetDinh(input_text)
    list_qd_view = []
    for i in list_qd:
        Attachresult = (
            "https://olt.mof.gov.vn/" + i["Attachresult"] if i["Attachresult"] else ""
        )
        temp = {
            "name": i["Numberaccept"],
            "Dateaccept_Char": i["Dateaccept_Char"],
            "iSoky": i["iSoky"],
            "Ngayky_CC": i["Ngayky_CC"],
            "SoLuongCC_Cap": i["SoLuongCC_Cap"],
            "Attachresult": Attachresult,
            "CreatDate": i["CreatDate"],
        }
        list_qd_view.append(temp)
    list_qd_view = pd.DataFrame(list_qd_view)
    list_qd_view.sort_values(by="CreatDate", inplace=True, ascending=False)
    list_qd_view.columns = [
        "Số quyết định",
        "Ngày cấp",
        "Số kỳ thi",
        "Ngày cấp CC",
        "Số lượng CC",
        "link",
        "date",
    ]
    list_qd_view.drop(columns=["date"], inplace=True)
    st.dataframe(list_qd_view, hide_index=True, width=2000)


if convert and input_text:
    showqd(input_text)
    list_qd = main.GetListSoQuyetDinh(input_text)
    try:
        list_contest = list_qd[0]["Codeofcourses"]
        st.markdown(f"DS cuộc thi: **{list_contest}**")
        list_contest_id = list_qd[0]["CourseIds"].split(",")
        list_contest_code = list_qd[0]["Codeofcourses"].split(",")
        NumberAcceptResult = list_qd[0]["Numberaccept"]
        Dateaccept_Char = list_qd[0]["Dateaccept_Char"]
        count = 0
        count_contest = -1
        final = []
        for contest in list_contest_id:
            count_contest += 1
            result_contest = main.get_result_contest(contest)
            list_cert = main.get_cc_contest(contest)
            for i in result_contest:
                count += 1
                temp = {
                    "stt": count,
                    "user_name": i["FullName"],
                    "birthday": i["BirthdayFull"],
                    "sex": i["SexName"],
                    "CCCDNumber": i["CCCDNumber"],
                    "CCCDIssueDatePicker": i["CCCDIssueDatePicker"],
                    "CCCDIssuePlace": i["CCCDIssuePlace"],
                    "AddressName": i["AddressName"],
                    "code_contest": list_contest_code[count_contest],
                    "Mark": i["Mark"],
                    "NumberAcceptResult": "",
                    "Dateaccept_Char": "",
                    "Machungchi_Cap": "",
                    "NgaykyChungchi": "",
                    "link_cert": "",
                }

                if i["Result"] == "Đạt":
                    for x in list_cert:
                        if x["Id"] == i["Id"]:
                            Machungchi_Cap = x["Machungchi_Cap"]
                            NgaykyChungchi = x["NgaykyChungchi"]
                            link_cert = (
                                r"https://olt.mof.gov.vn/Portal.iu.api//ChungChiSo/ChungChiSoDaKy/"
                                + x["TENFILE_KY"]
                                + ".pdf"
                            )
                            break
                    temp.update(
                        {
                            "NumberAcceptResult": NumberAcceptResult,
                            "Dateaccept_Char": Dateaccept_Char,
                            "Machungchi_Cap": Machungchi_Cap,
                            "NgaykyChungchi": NgaykyChungchi,
                            "link_cert": link_cert,
                        }
                    )
                final.append(temp)
        # st.write(final)
        final = pd.DataFrame(final)
        final.loc[final["Mark"] == -1, "Mark"] = ""
        final.columns = [
            "STT",
            "Họ và tên",
            "Ngày sinh",
            "Giới tính",
            "Số CCCD/CMT",
            "Ngày cấp",
            "Nơi cấp",
            "Đc thường trú",
            "Mã kỳ thi",
            "Điểm",
            "Số QĐ phê duyệt KQ thi",
            "Ngày cấp QĐ phê duyệt KQ thi",
            "Số chứng chỉ BVLN",
            "Ngày cấp chứng chỉ",
            "Link CC",
        ]

        st.dataframe(final, width=2000, hide_index=True)

    except:
        st.write("Có lỗi")
else:
    showqd("")
