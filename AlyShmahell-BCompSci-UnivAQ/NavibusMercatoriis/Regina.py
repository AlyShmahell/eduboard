# -*- coding: utf-8 -*-
import os
import sys
from bottle import route,run,template


# table start
stable = '<table>'
# table end
etable = '</table>'
# row start
srow = '<tr>'
# row end
erow = '</tr>'
# column title
colt = '<th>{{value}}</th>'
# cell data
celld = '<td>{{value}}</td>'

# start select
sselect = '<select name="{{selectName}}">'
# end select
eselect = '</select>'
# select body
selectb = '<option value="{{optionValue}}">{{optionValue}}</option>'

class Regina(object):
	def createTable(self,headArray, bodyArray):
	
		table = stable + srow
		for i in range(len(headArray)):
			table += template(colt, value = headArray[i])
		table += erow
		
		i=0
		while i < len(bodyArray):
			table+=srow
			for j in range(i,i+len(headArray)):
				table += template(celld, value = bodyArray[j])
			i += len(headArray)
			table += erow
		table += etable
		
		return table

	def createSelect(self, name, valuesArray):
		select = template(sselect, selectName = name)
		for i in range(len(valuesArray)):
			select += template(selectb, optionValue = valuesArray[i])
		select += eselect
		return select
		
		
@route('/')
def hello():
	rg = Regina()
	return rg.createTable(['title1','title2'],['data1','data2']) + rg.createSelect(4,['Hala','cow','Aly','Donkey'])
    
if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)
