import mailbox
mbox = mailbox.mbox("/path_to_text_file")
for message in mbox:
  print "from :",message['from']
  for key in message.keys():
    print key," :",message[key]
  content = ""
  if message.is_multipart():
    content = ''.join(part.get_payload(decode=False) for part in message.get_payload())
  else:
    content = message.get_payload(decode=False)
  print "content :",content