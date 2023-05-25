#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import re


# In[3]:


mydata = pd.read_json("contacts.json")


# In[4]:


mydata


# In[7]:


mydata['Email'].unique()
mydata['Phone'].unique()
mydata['OrderId'].unique()


# In[29]:


#form lists of unique variables
lst_email = mydata['Email'].unique().tolist()
lst_phone = mydata['Phone'].unique().tolist()
lst_orderid = mydata['OrderId'].unique().tolist()


# In[30]:


#remove white spaces
lst_email.remove('')
lst_phone.remove('')
lst_orderid.remove('')


# In[96]:


#form a dictionary with email as key and empty list as value
dict_email = {}
for email in lst_email:
    dict_email[email]= set()
for i in range(500000):
    email = mydata['Email'][i]
    if email in dict_email.keys():
        dict_email[email].add(i)


# In[100]:


#form phone dictionary
dict_phone= {}
for phone in lst_phone:
    dict_phone[phone]= set()
for i in range(500000):
    phone = mydata['Phone'][i]
    if phone in dict_phone.keys():
        dict_phone[phone].add(i)


# In[101]:


#form orderid dictionary
dict_orderid = {}
for order in lst_orderid:
    dict_orderid[order]=set()
for i in range(500000):
    orderid = mydata['OrderId'][i]
    if orderid in dict_orderid.keys():
        dict_orderid[orderid].add(i)


# In[177]:


#form ticket id dictionary
unique_Id = mydata['Id'].unique()
final_results = {id: set() for id in unique_Id}


# In[178]:


#getting the ticket id(s) for each unique id inside dictionary
dicts = [dict_email, dict_phone, dict_orderid]
for d in dicts:
    for key in d:
        key_set = d[key]
        for value in key_set:
            final_results[value] = final_results[value] | key_set


# In[228]:


final_results


# In[269]:


#list of ticket_trace for each unique_id
lst_trace = []
lst_of_ids = []
for key,sets in final_results.items():
    temp = list(sets)
    lst_of_ids.append(temp)
    if len(temp)>1:
        temp.sort()
        temp = [str(i) for i in temp]
        temp = '-'.join(temp)
        lst_trace.append(temp)
    else:
        lst_trace.append(str(temp[0]))


# In[283]:


#combining total contacts and ticket_trace into list
for index in range(len(lst_of_ids)):
    total = 0
    for i in lst_of_ids[index]:
        total+=mydata['Contacts'][i]
    lst_trace[index] = lst_trace[index] + ', ' + str(total)

lst_trace


# In[287]:


#making the final dataframe
data = {'ticket_id': unique_Id,
     'ticket_trace/contact': lst_trace}
df = pd.DataFrame(data, columns = ['ticket_id','ticket_trace/contact'])


# In[288]:


#make csv file for submission
df.to_csv('final.csv', index=False)

