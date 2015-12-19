import mailbox
import json
import datetime
import code
import sys
import os.path
import glob
from elasticsearch import Elasticsearch
from dateutil import parser

#TODO: Try to use a logger and a proper OO structure for ES and parser.

def sanitize_key_value(key, key_value):
  options = { "From" : sanitize_from,
              "Date" : sanitize_date,
              "Subject" : sanitize_subject,
              "References" : sanitize_ref_or_reply,
              "In-Reply-To" : sanitize_ref_or_reply,
              "Message-ID" : sanitize_message_id
  }
  return options[key](key_value)

def sanitize_from(original_value):
  return get_email(original_value)

def sanitize_date(original_value):
  return iso_date(original_value)

def sanitize_subject(original_value):
  return original_value

def sanitize_ref_or_reply(original_value):
  temp = original_value.split("\n\t")
  ret_val = []
  for val in temp:
    ret_val.append(remove_tag(val))
  return ret_val

def sanitize_message_id(original_value):
  return remove_tag(original_value)

# dateutil library solves the problem with time format inconsistency.
# datetime.isoformat() generates yyyy- MM-dd'T'HH:mm:ss.SSSZZ. which is compatible with date_time field of es.
# user name is yet to be included in the dictionary.
def put_to_es(dictionary):
  es = Elasticsearch([{'host': 'localhost', 'port': 9200}]) #should try to put it in some constant instead of everytime init
  index = 'ilugc_archives' #ideally this should be in some constant.
  doc_type = "email"
  #code.interact(local=dict(globals(), **locals()))
  doc_id = dictionary["Message-ID"]
  dictionary.pop("Message-ID")
  body = json.dumps(dictionary)
  try:
    es.index(index=index, doc_type=doc_type, id=doc_id, body=json.loads(body)) #fine out why without equal to assignment in argument it is not working.
  except:
    e = sys.exc_info()[0]
    print "******ERROR while pushing to ES******"
    print str(e)
    print "\n"
    print body


def remove_tag(str_data):
  if str_data[0] == "<" and str_data[-1] == ">":
    str_data = str_data[1:-1];
  else:
    print "This string does not have starting and ending tag: " + str_data
    return ""
  return str_data

def get_name(str_data):
  if str_data.index("(") and str_data.rindex(")"):
    str_data = str_data[str_data.index("(") + 1:str_data.rindex(")")]
  else:
    str_data = ""
  return str_data

def get_email(str_data):
  temp = str_data.split("(")
  email = ""
  if len(temp) > 1:
    email = temp[0].replace(" at ", "@")
  else:
    print str_data + " is not a valid email address."
  return email.replace(" ","")

def iso_date(time_str):
  temp = parser.parse(time_str)
  return temp.isoformat()

def get_content(message):
  content = ""
  if message.is_multipart():
    content = ''.join(part.get_payload(decode=False) for part in message.get_payload())
  else:
    content = message.get_payload(decode=False)
  return content


source_dir = os.path.dirname(os.path.abspath(__file__)) + "/archives/"

#One time case, remove this and make it to get the current month archive alone once legacy archives are pushed.
for src_name in glob.glob(os.path.join(source_dir, '*.txt')):
  try:
    mbox = mailbox.mbox(src_name)
    for message in mbox:
      dictionary = {}
      for key in message.keys():
        dictionary[key] = sanitize_key_value(key, message[key])
      if not dictionary.has_key("Message-ID"):
        print "*****No message id for the dictionary ******"
        print str(message)
        continue
      dictionary['content'] = get_content(message)
      put_to_es(dictionary)
  except:
    print "ERROR: with " + src_name