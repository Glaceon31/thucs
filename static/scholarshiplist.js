function showscholarshiplist(){
	d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')

	$.ajax({
      type:"POST",
      url:"/getscholarshiplist",
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)

          infolist = ['username','name','A','B','C','O','patent',
			'academic','shegong','total']
			for (j in result){
				scholarinfo = result[j]
				content = "<td>"+(j+1)+"</td>"
	          for (i=0;i<infolist.length;i++){
	            info = infolist[i]

	            content += "<td>"+scholarinfo[info]+"</td>"
	          }
	          content += "<td>0</td>"
	          content += "<td><a href='/scholarshipview/"+scholarinfo['username']+"'>查看</a></td>"
	          $("#applylist_addr"+j).html(content)
	          $("#applylist").append('<tr id="applylist_addr'+(j+1)+'"></tr>')
			}
      }
    })

}