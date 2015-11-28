import mailbox
import json

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
  return ist_iso_date(original_value)

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

# TODO: Observe the dicionary for inconsistency in archives formats.
# To Handle: Time is breaking because of inconsistant time format on the archive.
# 'Sat, 11 Dec 2010 15:55:48 +0530 (IST)' does not match format '%a %b  %d %H:%M:%S %Y'
# user name is yet to be included in the dictionary.
def put_to_es(dictionary):
  temp = json.dumps(dictionary)
  print "****"
  print temp
  print "****"


def remove_tag(str_data):
  if str_data[0] == "<" and str_data[-1] == ">":
    str_data = str_data[1:-1];
  else:
    print "This string does not have starting and ending tag: " + str_data
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

#TODO: Make the +05:30 more flexible for any time zone.
def ist_iso_date(time_str):
  import datetime
  from datetime import timedelta
  a = datetime.datetime.strptime(time_str, "%a %b  %d %H:%M:%S %Y")
  b = a + timedelta(hours=5, minutes=30)
  return b.isoformat()

def get_content(message):
  content = ""
  if message.is_multipart():
    content = ''.join(part.get_payload(decode=False) for part in message.get_payload())
  else:
    content = message.get_payload(decode=False)
  return content

mbox = mailbox.mbox("_path_to_file_")
for message in mbox:
  dictionary = {}
  for key in message.keys():
    dictionary[key] = sanitize_key_value(key, message[key])
  dictionary['content'] = get_content(message)
  put_to_es(dictionary)