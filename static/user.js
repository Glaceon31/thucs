function register(){
		if (document.getElementById('passwd').value.length < 8){
 	  		alert('密码长度至少为8')
 	  		return
 	  	}
		if (document.getElementById('passwd').value != document.getElementById('repasswd').value){
 	  		alert('两次密码不相同')
 	  		return
 	  	}
 	  	
		d = {}
		d['username'] = document.getElementById('username').value
		d['password'] = $.md5(document.getElementById('passwd').value)
		d['name'] = document.getElementById('name').value
		d['code'] = document.getElementById('code').value
		//d['postcode'] = document.getElementById('postcode').value
		
		$.ajax({
			type:"POST",
			url:"/userregister",
			data: d,
			success:function reg_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert(result['message'])
 	  			window.location = '/'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }
 	  
function login(){
 	  	d = {}
 	  	d['username'] = document.getElementById("username").value
 	  	d['password'] = $.md5(document.getElementById("passwd").value)
 	  	$.ajax({
			type:"POST",
			url:"/userlogin",
			data: d,
			success:function login_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			setCookie('useridthu', result['userid'], 10)
 	  			setCookie('usernamethu', result['username'], 10)
 	  			setCookie('tokenthu', result['token'], 10)
 	  			window.location = '/scholarship'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }

function checklogin(){
 	  	d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')

 	  	$.ajax({
			type:"POST",
			url:"/userchecklogin",
			data: d,
			success:function checklogin_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			//document.getElementById('information').style.display = ''
 	  		}
 	  		else{
 	  			alert('请先登录')
 	  			window.location = '/'
 	  		}
 	  	}
		})
 	  }

function showname(){
 	  	d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	$.ajax({
			type:"POST",
			url:"/getuserinfo",
			data: d,
			success:function userinfo_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){

 	  				document.getElementById('name').innerHTML=result['name']

 	  		}
 	  		else{
 	  		}
 	  	}
		})
 	  }

function showuserinfo(){
 	  	d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	$.ajax({
			type:"POST",
			url:"/getuserinfo",
			data: d,
			success:function userinfo_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			infolist = ['name','class','sex','school_roll','political','grade','suo'
 	  			,'ethnic','mas_doc','mentor','email', 'postcode','address','mobile']
 	  			for (i=0;i<infolist.length;i++){
 	  				info = infolist[i]
 	  				document.getElementById(info).value=result[info]
 	  			}
 	  		}
 	  		else{
 	  		}
 	  	}
		})
 	  }

 	  function logout(){
 	  	d = {}
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	delCookie('usernamethu')
 	  	delCookie('useridthu')
 	  	delCookie('tokenthu')
 	  	jsondata = JSON.stringify(d)
 	  	$.post('/logout/'+jsondata)
 	  	window.location = '/'
 	  }


function modify(){
		d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	infolist = ['name','class','sex','school_roll','political','grade','suo'
 	  			,'ethnic','mas_doc','mentor','email', 'postcode','address','mobile']
 	  	for (i=0;i<infolist.length;i++){
 	  				info = infolist[i]
 	  				d[info] = document.getElementById(info).value
 	  			}
		
		$.ajax({
			type:"POST",
			url:"/usermodify",
			data: d,
			success:function modify_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert(result['message'])
 	  			window.location = '/mainpage'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }

function modifypassword(){
		if (document.getElementById('newpasswd').value.length < 8){
 	  		alert('密码长度至少为8')
 	  		return
 	  	}
		if (document.getElementById('newpasswd').value != document.getElementById('repasswd').value){
 	  		alert('两次密码不相同')
 	  		return
 	  	}
 	  	
		d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
		d['oldpassword'] = $.md5(document.getElementById('oldpasswd').value)
		d['newpassword'] = $.md5(document.getElementById('newpasswd').value)
		
		$.ajax({
			type:"POST",
			url:"/usermodifypassword",
			data: d,
			success:function modifypassword_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert(result['message'])
 	  			window.location = '/mainpage'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }
