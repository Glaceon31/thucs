function showscholarshiplist(){
	d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')

    md = document.getElementById('mas_doc').value
    suo = document.getElementById('suo').value
    sort = document.getElementById('sort').value
	$.ajax({
      type:"POST",
      url:"/getscholarshiplist/"+md+"_"+suo+"_"+sort,
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)

          infolist = ['username','name','A','B','C','O','patent',
			'academic']//,'shegong','total']
			document.getElementById('listing').innerHTML = "<tr id='applylist_addr0'></tr>"
			for (j in result){
				scholarinfo = result[j]
				content = "<td>"+(parseInt(j)+1)+"</td>"
	          for (i=0;i<infolist.length;i++){
	            info = infolist[i]

	            content += "<td>"+scholarinfo[info]+"</td>"
	          }
	          content += "<td>"+parseInt(1000*scholarinfo['shegong'])/1000+"</td>"
	          content += "<td>"+parseInt(1000*scholarinfo['total'])/1000+"</td>"
	          content += "<td>"+scholarinfo['reported']+"</td>"
	          content += "<td><a href='/scholarshipview/"+scholarinfo['username']+"'>查看</a></td>"
	          if (scholarinfo['wrongtime'] || scholarinfo['invalid']){
	          	document.getElementById('applylist_addr'+(parseInt(j))).style.color='red'
	          }
	          $("#applylist_addr"+j).html(content)
	          $("#applylist").append('<tr id="applylist_addr'+(parseInt(j)+1)+'"></tr>')
			}
      }
    })

}

$(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
})