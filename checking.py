from io import StringIO

import streamlit as st
from streamlit_ace import st_ace

st.title("Stack Overflow Auto-Search Tool")

st.text(
    'Instruction:' + '\n''1. Select a Code File' + '\n''2. Click the Search Button(Ctrl+Q)' + '\n''3. You will get all the err solutions for the selected code file')

from subprocess import Popen, PIPE
import requests
import webbrowser

code = ""
string_data =""

uploaded_file = st.file_uploader('File upload')


if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.write(dataframe)

first,second = st.columns(2)

with first:
    code = st_ace()

with second:
    st.write(code)

def creating2File(code):
    p = open("test.py","w")
    p.write(code)
    p.close()
    code="code"
    st.write(code)

def getData(cmd):
    cmd_list = cmd.split()
    print(cmd_list)
    process = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    return out, err

def make_request(err):
    print("Searching for " + err)
    response = requests.get(
        "https://api.stackexchange.com" + "/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(err))
    return response.json()


def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == 3 or count == len(i):
            break
    for i in url_list:
        webbrowser.open(i)

def creatingFile(string_data):
    f=open('test.py','w')
    f.write(string_data)  
    f.close()
    string_data="string_data"
    st.write(string_data)

        


def autoSearch():
    if __name__ == "__main__":

     if(len(code) != 0 ) or (len(string_data) != 0):
        if(len(string_data)==0):
            creating2File(code)
            st.write(code)
            
        else:
            creatingFile(string_data)
            st.write(string_data)

     else:
        st.write("Please upload a file or enter your text on text editor")

     out, err = getData("python test.py")
     print("python {}".format(uploaded_file))
     err = err.decode("utf-8").strip().split("\r\n")[-1]
     print("err => ", err)
     print(getData("python {}".format(uploaded_file)))
     
    if (err):
        err_list = err.split(":")
        json1 = make_request(err_list[0])
        json2 = make_request(err_list[1])
        json3 = make_request(err)
        get_urls(json1)
        get_urls(json2)
        get_urls(json3)
    else:
        print("No err")

st.button("Search", on_click=autoSearch)