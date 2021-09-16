#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pprint
import math
import tkinter

from nltk.stem import WordNetLemmatizer

# from nltk.tokenize import word_tokenize

# import nltk
# nltk.download()


# In[2]:


# list data read all file Data
data = []
file = []
index = {}
term_frequency = {}
word = []
document_frequency = {}
inverse_doc_frequency = {}
weight = {}
vector = {}
doc_query = {}
result = []
cosine_angle = {}
temp_dict = {}
i = 0
variable = ''

lemitization = WordNetLemmatizer()
m = tkinter.Tk()


# In[3]:


# Reading the data
path: str = r"D:\Assignment_01_IR\ShortStories"  # Path to read files of short stories
for filename in os.listdir(path):
    full_path = os.path.join(path, filename)  # evaluating Path of all File
    with open(full_path, encoding="utf-8") as f:
        file_data = f.read()
        data.append(file_data)  # appending the file_data in data list
        # print(filename)
        file.append(filename)
    i = i + 1


# In[4]:


def word_break(arr):  # Breaking the lines into words of all file
    dat = []
    element = ''
    for m in range(len(arr)):  # Conditions to break Words
        if arr[m] == ' ' or arr[m] == ',' or arr[m] == '.' or arr[m] == '\n' or arr[m] == '"' or arr[m] == '?' or                 arr[m] == ';' or arr[m] == ':' or arr[m] == '!' or arr[m] == '-' or arr[m] == '—' or arr[m] == '“'                 or arr[m] == '”' or arr[m] == '(' or arr[m] == ')':
            if element == '”' or element == ' ' or element == ':' or element == '!':
                element = ''
                continue
            else:
                dat.append(element.replace('!', '').replace('\n', '').replace('"', '').replace('?', '').replace('“', '')
                           .replace(';', '').lower())  # appending data in dat list
            element = ''  # removing previous word from element
            continue

        element = element + arr[m]  # entering word in element from data list
        for n in range(len(element)):
            if element[n] == '”':
                element[n].replace('”', '1')
    for j in range(dat.count('')):
        dat.remove('')
    # print(dat)
    arr = dat
    return arr  # returning the list which is converted into individual word


# In[5]:


def stop_words(arr):  # removing stop words from data list
    ft = open("D:\\Assignment_01_IR\Stopword-List.txt ", "r")  # path to read stop words
    stopwords = ft.read()
    stopwords = word_break(stopwords)  # entering stop words in to stopwords list
    for n in range(len(stopwords)):
        counts = arr.count(stopwords[n])  # counting specific stop words in a file
        for o in range(counts):
            arr.remove(stopwords[n])  # removing stop words from a file one by one (file)
    return arr  # returning the whole data list named as arr in this function


# In[6]:


def Lemitization_func():
    for l_data in range(len(data)):
        for w_data in range(len(data[l_data])):
            data[l_data][w_data] = lemitization.lemmatize(data[l_data][w_data])


# In[7]:


def convert_Dictionary_1():  # converting data into dictionary with key as a file name
    for i in range(len(data)):
        index[file[i]] = data[i]  # index is a dictionary to insert data as dictionary


# In[8]:


def word_find(arr, word_f):  # finding word from specific file or whole data list
    i = 0
    for i in range(len(arr)):
        if arr[i] == word_f:  # arr is a document and word_f is a word to be find
            return True  # if word found then return true else return false
    return False


# In[9]:


def Term_frequency_1(g):  #Calulating Term Frequency
    get_data=[]
    dict_data={}
    for h in file:
        if g in index[h]:
            dict_data.update({h: math.log(1+index[h].count(g))})  #By using Formula log(1+tf) creating Term Frequency and returning to main function to add in dictionary term_frequency
    return dict_data    


# In[10]:


def Term_frequency():  # inverted index of data which is read from file
    for i in range(len(data)):
        for j in range(len(data[i])):
            # print(data[i][j])
            if data[i][j] not in word:
                word.append(data[i][j])  # appending data in word
                continue
    
    for g in range(len(word)):
        term_frequency[word[g]] = Term_frequency_1(word[g])  #get data calulaed data from  the function Term_frequency_1


# In[11]:


def Document_frequency():  #calculating Document Frequency
    count = 0
    for doc in range(len(word)):
        document_frequency[word[doc]] = len(term_frequency[word[doc]])  #Calculaing the documents containing certain words


# In[12]:


def Inverse_Document_frequency():  #calculating Inverse Document Frequency
    for f in range(len(word)):
        inverse_doc_frequency[word[f]] = math.log((len(file)/document_frequency[word[f]]),10)  #using formula log(N/df) for idf


# In[13]:


def Calculating_weight_1(w):  #calculating score or weigth
    value = inverse_doc_frequency[w]
    dict_weight = {}
    for h in term_frequency[w]:
        dict_weight.update({h: value*term_frequency[w][h]})  # calculating tf*idf
    return dict_weight   


# In[14]:


def Calculating_weight():
    for scre1 in word:
        weight[scre1] = Calculating_weight_1(scre1)  #appending to dictionary calculated tf*idf


# In[15]:


def Vector_development_1(D):  #making Vector into all documents for processing
    temp = []
    for wrd in word:
        if D in weight[wrd]:
            temp.append(inverse_doc_frequency[wrd])  #appending the word value if D is in word doc
        else:
            temp.append(0)
    return temp


# In[16]:


def Vector_development():
    for Doc in file:
        vector[Doc] = Vector_development_1(Doc)  #appending the vector in vector dictionary


# In[17]:


def Vector_development_query(query):  #Query into Vector same as document
    temp = []
    for wrd in word:
        if wrd in query:
            temp.append(inverse_doc_frequency[wrd])
        else:
           temp.append(0) 
    return temp


# In[18]:


def Processing_query(query):  #processing the query and evaluating cosine angle
    for doc in vector:  #calculating Doc*Query
        temp = 0
        for que in range(len(query)):
            temp = temp + vector[doc][que]*query[que]
        doc_query[doc] = temp 
    temp_q=0
    for size in range(len(query)):  #calculating (sum of all (query^2))^1/2
        temp_q=temp_q+query[size] ** 2
    temp_q=math.sqrt(temp_q)
    print(temp_q)
    temp1 = 0
    
    
    for doc in vector:  #calculating (sum of all (vector^2))^1/2
        temp2 = 0
        for que in range(len(vector[doc])):
            temp2 = temp2 + vector[doc][que] ** 2
        temp2 = math.sqrt(temp2)
        temp_dict[doc] = temp2
    
    for doc in vector:  #calculating Cosine angle
        tmp = 0
        tmp = (doc_query[doc]/(temp_q*temp_dict[doc]))
        print("document * query",doc_query[doc],"query Vector",temp_q,"temp_dict",temp_dict[doc])
        cosine_angle[doc] = tmp
    


# In[19]:


for k in range(len(data)):
    data[k] = word_break(data[k])  # word break from files
print("Word Break Completed")
for a in range(len(data)):
    data[a] = stop_words(data[a])  # removing stop words from data
print("Removing Stop Words Comleted")


# In[20]:


Lemitization_func() # performing lemitization
print("Lemitization Completed")
convert_Dictionary_1()# Own usage function
Term_frequency()
print("Term Frequeny Created")
Document_frequency()
print("Document Frequency Created")
# for d in index:
#     sume = sume+len(index[d])
    
# print(len(word))


# In[142]:


def show_entry_fields():
    query = (e1.get())
    query = word_break(query)
    query = stop_words(query)
    print(query)
    for loop in range(len(query)):
        query[loop] = lemitization.lemmatize(query[loop])
    print(query)
    quew = len(query)
    query = Vector_development_query(query)
    Processing_query(query)
    s =0 
    result = []
    for size in file:
        if cosine_angle[size] > 0.005:
            result.append(size)
            s=s+1
    print(result)
    #messagebox.showinfo(message = result[ln])
    lsum = Label(master, text = 'The Result of Document is : ')
    lsum.grid(row=5, column=0, sticky=W, pady=4)
    lsum = Label(master, text = ('Number of obtained Documents : ',s))
    lsum.grid(row=6, column=0, sticky=W, pady=4)
    lsum = Label(master, text = ('Number of Words : ',quew))
    lsum.grid(row=7, column=0, sticky=W, pady=4)
    for ln in range(len(result)):
        lsum = Label(master, text = result[ln]+'\n')
        lsum.grid(row=8+ln, column=0, sticky=W, pady=4)
    


# In[56]:


Inverse_Document_frequency()
print("Inverse Document Frequency Created")
#weight = term_frequency
weight = term_frequency.copy()
Calculating_weight()
print("Weight/Scores Created")
Vector_development()
print("Document Vector Created")
#pprint.pprint(inverse_doc_frequency)


# In[148]:


from tkinter import *
from tkinter import messagebox

master = Tk()
master.config(bg='lightgreen' ,height=1000,width=2000)
Label(master, 
         text="Search Here").grid(row=0)
w = Scale(master, from_=0, to=100000)

e1 = Entry(master)

e1.grid(row=0, column=1)

Button(master, 
          text='Quit', 
          command=master.quit).grid(row=3, 
                                    column=0, 
                                    sticky=W, 
                                    pady=4)
Button(master, 
          text='Show', command=show_entry_fields).grid(row=3, 
                                                       column=1, 
                                                       sticky=W, 
                                                       pady=4)
mainloop()

