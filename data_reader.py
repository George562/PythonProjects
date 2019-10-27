try:
	from xml.dom import minidom
	data = minidom.parse('data.xml')
	r = data.read()
	input(r['number'])
except Exception as e:
	input(e)