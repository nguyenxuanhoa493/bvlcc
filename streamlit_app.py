import streamlit as st
import requests, time, json
import pandas as pd

def current_time_ts():
    return "&_="+str(int(time.time()*1000))

class Cc:
    def __init__(self) -> None:
        self.api = "https://olt.mof.gov.vn/Portal.IU.API/api/"
        self.payload = {}
        self.headers = {
        'authority': 'olt.mof.gov.vn',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json; charset=utf-8',
        'cookie': 'SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; ASP.NET_SessionId=nm0izer4k2jymaenvagcufcf; __AntiXsrfToken=d47f052ea4cc4308b77a90f3779b9909; .Auth=C0FF8A2E049D156CAF69B5826FCAC606D06278A8398745D65B9936C0466D036B69700EFC43272E0A027A3A9034C5C2534D2317536F68D82A1445D0E89066D8341D2E5EBDFF14A3B057F99368506C25641A3EB18366675BD98AFFC0BD969274F4BB857211FFDCD752E1919751EBF4E72AB86FFD81FA7420F81D68531761EB3D9DBF4EC284C99DF77A0AA02EDF5CDFF021B50339F6947B10B5B9C368478B9F31A31ECC6BF34D7FEA3EFE23FBEDF38FCA51924AAA48AE08862FCE29BF44CF43C14536C11321D76A576D607289DC7A4E9CC78D0AF597A8A892BF44F426CC1A9FEC3921D8D033496019DF4B3C0E7B5E87A70DC89823E334BD502DC4945191EF54CBE36475534067A39E5DF5CB8BFB6A9F6A8A617C0B2C09D66C196D19C17E988360AAAD5695DA66A42C416637C4C3EDFB11ED4D83049FEAAC466C7BC751B17365441BC42FB83DC6B42D23FAC8810492B581E83186A1755AEB26863EBCEDCA5A1C85C1926675F205DBC3A7F8BD662B6ACABDC855AAFCB60EECAA0F0ED7B12D2A293DBB2CCF44B89C13143B57DA674E70F78ADA4D5265513F1564A2A6F13902EB532F2B58580F13A82E8932FE13113E7E8242F5EC5A6FDDAB40D50587E321D56712347013066F2E7D3610887F7C4BE783DB06A7AC724248DDF79CD2304971E59ADCF20F05CFBDFE831BCCCBAF99F228CD0C2C937953EBF428FB08AFE0759363CD1C84919086814F562B79E4A40EC545FEFD360FAEC71CE3D825A6249E8001BE025F801A362D391A73EE02E3BA778CB06711DA85598EDCACD5321CF4B742D428D060FDAB37E19B0DB5C8EA27136589D1143621AA3997AABA4F7B3F88F66E418C2FEE4AAC',
        'referer': 'https://olt.mof.gov.vn/Portal.IU.CMS/Default.aspx',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }
    
    def send(self, url):
        response = requests.request("GET", self.api+url+current_time_ts(), headers=self.headers, data=self.payload)
        return response.json()

    def GetListSoQuyetDinh(self,key=""):
        url = r"/DocumentAcceptNumber/GetListSoQuyetDinhByCom?strTuKhoa="+key+r"&pageIndex=1&pageSize=10000&iTrangThai=2&FromDate=01%2F01%2F2022&ToDate=12%2F31%2F2023&Companyid=79226B0E4C85415ABDFE9CD719BA0962&User_id=&Managecategory_id=" 
        response = self.send(url) 
        return response['Data']

    def get_id_contest_by_code(self, code_contest):
        url = r"Course/getListAcc?keyword=2.1.1011.002599&companyId=%3B79226B0E4C85415ABDFE9CD719BA0962&companySubId=&provinceId=&fromDate=11%2F02%2F1970&toDate=11%2F07%2F2023&status=8&examType=&pageIndex=1&pageSize=1"
        response = self.send(url)   
        try:
            return response['Data'][0]
        except:
            return False
        
    def get_result_contest(self, id_contest):
        url = r"Staff/getStaffByCourseId?courseId="+id_contest
        response = self.send(url)   
        try:
            return response['Data']
        except:
            return False
        
    def get_cc_contest(self, id_contest):
        url = r"Staff/GetStaffCertByCourseId?courseId="+id_contest
        response = self.send(url)   
        try:
            return response['Data']
        except:
            return False

        
main = Cc()



print(json.dumps(main.GetListSoQuyetDinh('45/QĐ-QLBH'),  indent=4, sort_keys=True,ensure_ascii=False))

st.set_page_config(page_title="BVL download CC",layout='wide')
st.title("Tải kết quả")
with st.form(key='my_form'):
    c1, c2= st.columns([7,3])

    with c1:
        input_text = st.text_input('Mã quyết định:')
    with c2:
        convert = st.form_submit_button('tìm kiếm')

def showqd(input_text):
    list_qd = main.GetListSoQuyetDinh(input_text)
    list_qd_view = []
    for i in list_qd:
        Attachresult = "https://olt.mof.gov.vn/"+i['Attachresult'] if i['Attachresult'] else ""
        temp = {
            'name':i['Numberaccept'],
            'Dateaccept_Char':i['Dateaccept_Char'],
            'iSoky':i['iSoky'],
            'Ngayky_CC':i['Ngayky_CC'], 
            'SoLuongCC_Cap':i['SoLuongCC_Cap'], 
            'Attachresult':Attachresult,
            'CreatDate':i['CreatDate']
        }
        list_qd_view.append(temp)
    list_qd_view = pd.DataFrame(list_qd_view)
    list_qd_view.sort_values(by="CreatDate",inplace=True, ascending=False)
    list_qd_view.columns = ['Số quyết định', 'Ngày cấp', 'Số kỳ thi', 'Ngày cấp CC', 'Số lượng CC', 'link', 'date']
    list_qd_view.drop(columns=['date'], inplace=True)
    st.dataframe(list_qd_view, hide_index=True,  width=2000)

if convert and input_text:
    showqd(input_text)
    list_qd = main.GetListSoQuyetDinh(input_text)
    try:
        list_contest = list_qd[0]['Codeofcourses']
        st.markdown(f"DS cuộc thi: **{list_contest}**")
        list_contest_id = list_qd[0]['CourseIds'].split(',')
        list_contest_code = list_qd[0]['Codeofcourses'].split(',')
        NumberAcceptResult = list_qd[0]['Numberaccept']
        Dateaccept_Char = list_qd[0]['Dateaccept_Char']
        count=0
        count_contest = -1
        final = []
        for contest in list_contest_id:
            count_contest+=1
            result_contest = main.get_result_contest(contest)
            list_cert = main.get_cc_contest(contest)
            for i in result_contest:
                count+=1
                temp = {
                    'stt': count,
                    'user_name':i['FullName'],
                    'birthday': i['BirthdayFull'],
                    'sex': i['SexName'],
                    'CCCDNumber': i['CCCDNumber'],
                    'CCCDIssueDatePicker': i['CCCDIssueDatePicker'],
                    'CCCDIssuePlace': i['CCCDIssuePlace'],
                    'AddressName': i['AddressName'], 
                    'code_contest':list_contest_code[count_contest],
                    'Mark': i['Mark'], 
                    'NumberAcceptResult':"",
                    'Dateaccept_Char':"",
                    'Machungchi_Cap':"",
                    'NgaykyChungchi':"",
                    'link_cert':""
                }

                if i['Result'] == 'Đạt':
                    for x in list_cert:
                        if x['Id'] == i['Id']:
                            Machungchi_Cap= x['Machungchi_Cap']
                            NgaykyChungchi = x['NgaykyChungchi']
                            link_cert = r"https://olt.mof.gov.vn/Portal.iu.api//ChungChiSo/ChungChiSoDaKy/"+x['TENFILE_KY']+".pdf"
                            break
                    temp.update(
                        {   
                            'NumberAcceptResult':NumberAcceptResult,
                            'Dateaccept_Char': Dateaccept_Char,
                            'Machungchi_Cap':Machungchi_Cap,
                            'NgaykyChungchi':NgaykyChungchi,
                            'link_cert':link_cert
                        }
                    )
                final.append(temp)
        # st.write(final)
        final = pd.DataFrame(final)
        final.loc[final['Mark'] == -1, 'Mark'] = ""
        final.columns = ['STT', 'Họ và tên', 'Ngày sinh', 'Giới tính', 'Số CCCD/CMT', 'Ngày cấp', 'Nơi cấp', 'Đc thường trú', 'Mã kỳ thi', 'Điểm', 'Số QĐ phê duyệt KQ thi', 'Ngày cấp QĐ phê duyệt KQ thi', 'Số chứng chỉ BVLN', 'Ngày cấp chứng chỉ', 'Link CC']

        st.dataframe(final, width=2000, hide_index=True)
        
    except:
        st.write("Có lỗi")
else:
    showqd("")


