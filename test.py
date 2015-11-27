import mailbox
mbox = mailbox.mbox("/path_to_text_file")
for message in mbox:
  #print "from :",message['from']
  #dictionary = { 'from' : message['from'] }
  for key in message.keys():
    print key," :",message[key]
    dictionary[str(key)] = message[key]
  content = ""
  if message.is_multipart():
    content = ''.join(part.get_payload(decode=False) for part in message.get_payload())
  else:
    content = message.get_payload(decode=False)
  print "content :",content
  dictionary['content'] = content
  put_to_elastic_search(dictionary)


def put_to_elastic_search(dictionary):
  from_email = dictionary["From"] #have to parse email from the full text.
  name = dictionary["From"] #have to get name from that using regex.
  date = dictionary["Date"] #have to format to ISO  8601 and add +530
  content = dictionary["content"]
  subject = dictionary["Subject"]
  in_reply_to = dictionary["In-Reply-To"] #have to analyse how multiple entries are put and remove '<', '>'
  references = dictionary["References"] #have to analyse how multiple entries are put and remove '<', '>'
  message_id = dictionary["Message-ID"] #have to remove '<', ">"


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
  #split the string by (, get the first index, in the first index find ' at ' and substitue it by @ symbol.

#TODO: Make the +05:30 more flexible for any time zone.
def ist_iso_date(time_str):
  import datetime
  from datetime import timedelta
  a = datetime.datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S +0530")
  b = a + timedelta(hours=5, minutes=30)
  return b.isoformat()




