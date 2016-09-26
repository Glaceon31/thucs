function applycancel(){
  d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')
      $.ajax({
      type:"POST",
      url:"/scholarshipcancel",
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)
        if (result['success'] == 1){
          alert(result['message'])
          window.location='/scholarshipapply'
        }
        else{
          alert(result['message'])
        }
      }
    })
    }

function getbasicinfo(){
      d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')
      document.getElementById('username').value=d['username']
      document.getElementById('token').value=d['token']
      document.getElementById('username').readOnly=true
      $.ajax({
      type:"POST",
      url:"/getuserinfo",
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)
        if (result['success'] == 1){
          infolist = ['name','class','sex','school_roll','political','grade','suo'
          ,'ethnic','mas_doc','mentor','email','mobile']
          for (i=0;i<infolist.length;i++){
            info = infolist[i]
            document.getElementById(info).value=result[info]
            document.getElementById(info).readOnly=true
          }
        }
        else{
        }
      }
    })
    }


function getscholarshipinfo(){
  
      d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')
      
      $.ajax({
      type:"POST",
      url:"/getscholarshipinfo/"+d['username'],
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)
        if (result['success'] == 1){
          result = JSON.parse(result['scholarshipinfo'])
          //inputinfo
          infolist = ['tice','otheraward','kaiti']
          for (i=0;i<infolist.length;i++){
            info = infolist[i]
            //if (result.has_key(info)){
              document.getElementById(info).value=result[info]
            //}
          }
          //tableinfo
          infolist=['conf','qikan','patent','project','standard','confaward','job','accupro']
          infosublist=[['author','yizuo','CCF','conf','paper','time','pages', 'papertype','lastyear'],
          ['author','CCF','qikan','paper','time','pagenum','pages', 'papertype','lastyear'],
          ['author','patent','publishid','time','lastyear'],
          ['author','project','time','type','lastyear'],
          ['author','standard','time','lastyear'],
          ['author','confaward','conf','CCF','time','lastyear'],
          ['job','level','starttime','endtime','months'],
          ['accupro','content','time']
          ]
          for (ind=0;ind<infolist.length;ind++){
            num = 0
            info = infolist[ind]
            sublist = infosublist[ind]

            while (result[info+"_"+sublist[0]+num]){
                $("#"+info+"_add_row").click()
                for (j=0;j<sublist.length;j++){
                  document.getElementById(info+"_"+sublist[j]+num).value=result[info+"_"+sublist[j]+num]
                }
              num += 1
            }
          } 
        }
        else{
        }
      }
    })
}


$(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 

      var conf_i=0;
     $("#conf_add_row").click(function(){
      $('#conf_addr'+conf_i).html("<td>"+ (conf_i+1) 
        +"</td><td><input type='text' name='conf_author"+conf_i
        +"' id='conf_author"+conf_i
        +"' class='form-control px150'/> </td><td><select name='conf_yizuo"+conf_i
        +"' id='conf_yizuo"+conf_i
        +"' class='form-control px50'/></select>"
        +"</td><td><select name='conf_CCF"+conf_i
        +"' id='conf_CCF"+conf_i
        +"' class='form-control px50'/></select>"
        +"</td><td><input type='text' name='conf_conf"+conf_i
        +"' id='conf_conf"+conf_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='conf_paper"+conf_i
        +"' id='conf_paper"+conf_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='conf_time"+conf_i
        +"' id='conf_time"+conf_i
        +"' class='form-control px100'/>"
        +"</td><td><input type='text' name='conf_pages"+conf_i
        +"' id='conf_pages"+conf_i
        +"' class='form-control px50'/>"
        +"</td><td><select name='conf_papertype"+conf_i
        +"' id='conf_papertype"+conf_i
        +"' class='form-control px100'/></select>"
        +"</td><td><select name='conf_lastyear"+conf_i
        +"' id='conf_lastyear"+conf_i
        +"' class='form-control px100'/></select></td>");

      $('#conf').append('<tr id="conf_addr'+(conf_i+1)+'"></tr>');
      document.getElementById("conf_yizuo"+conf_i).add(new Option("是","是"))
      document.getElementById("conf_yizuo"+conf_i).add(new Option("否","否"))
      document.getElementById("conf_CCF"+conf_i).add(new Option("A","A"))
      document.getElementById("conf_CCF"+conf_i).add(new Option("B","B"))
      document.getElementById("conf_CCF"+conf_i).add(new Option("C","C"))
      document.getElementById("conf_CCF"+conf_i).add(new Option("O","O"))
      document.getElementById("conf_CCF"+conf_i).add(new Option("其他","其他"))
      document.getElementById("conf_papertype"+conf_i).add(new Option("full paper","full paper"))
      document.getElementById("conf_papertype"+conf_i).add(new Option("poster","poster"))
      document.getElementById("conf_papertype"+conf_i).add(new Option("short paper","short paper"))
      document.getElementById("conf_papertype"+conf_i).add(new Option("workshop","workshop"))
      document.getElementById("conf_papertype"+conf_i).add(new Option("demo","demo"))
      document.getElementById("conf_lastyear"+conf_i).add(new Option("否","否"))
      document.getElementById("conf_lastyear"+conf_i).add(new Option("是","是"))
      
      conf_i++; 
  });
     $("#conf_delete_row").click(function(){
       if(conf_i>=1){
     $("#conf_addr"+(conf_i-1)).html('');
     conf_i--;
     }
   });

  var qikan_i = 0

  $("#qikan_add_row").click(function(){
      $('#qikan_addr'+qikan_i).html("<td>"+ (qikan_i+1) 
        +"</td><td><input type='text' name='qikan_author"+qikan_i
        +"' id='qikan_author"+qikan_i
        +"' class='form-control px150'/> </td><td><select name='qikan_CCF"+qikan_i
        +"' id='qikan_CCF"+qikan_i
        +"' class='form-control px50'/></select>"
        +"</td><td><input type='text' name='qikan_qikan"+qikan_i
        +"' id='qikan_qikan"+qikan_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='qikan_paper"+qikan_i
        +"' id='qikan_paper"+qikan_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='qikan_time"+qikan_i
        +"' id='qikan_time"+qikan_i
        +"' class='form-control px100'/>"
        +"</td><td><input type='text' name='qikan_pagenum"+qikan_i
        +"' id='qikan_pagenum"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><input type='text' name='qikan_pages"+qikan_i
        +"' id='qikan_pages"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><select name='qikan_papertype"+qikan_i
        +"' id='qikan_papertype"+qikan_i
        +"' class='form-control px100'/></select>"
        +"</td><td><select name='qikan_lastyear"+qikan_i
        +"' id='qikan_lastyear"+qikan_i
        +"' class='form-control px100'/></select></td>");

      $('#qikan').append('<tr id="qikan_addr'+(qikan_i+1)+'"></tr>');
      document.getElementById("qikan_CCF"+qikan_i).add(new Option("A","A"))
      document.getElementById("qikan_CCF"+qikan_i).add(new Option("B","B"))
      document.getElementById("qikan_CCF"+qikan_i).add(new Option("C","C"))
      document.getElementById("qikan_CCF"+qikan_i).add(new Option("O","O"))
      document.getElementById("qikan_CCF"+qikan_i).add(new Option("其他","其他"))
      document.getElementById("qikan_papertype"+qikan_i).add(new Option("full paper","full paper"))
      document.getElementById("qikan_papertype"+qikan_i).add(new Option("poster","poster"))
      document.getElementById("qikan_papertype"+qikan_i).add(new Option("short paper","short paper"))
      document.getElementById("qikan_papertype"+qikan_i).add(new Option("workshop","workshop"))
      document.getElementById("qikan_papertype"+qikan_i).add(new Option("demo","demo"))
      document.getElementById("qikan_lastyear"+qikan_i).add(new Option("否","否"))
      document.getElementById("qikan_lastyear"+qikan_i).add(new Option("是","是"))
      
      qikan_i++; 
  });
     $("#qikan_delete_row").click(function(){
       if(qikan_i>=1){
     $("#qikan_addr"+(qikan_i-1)).html('');
     qikan_i--;
     }
   });

  var patent_i = 0

  $("#patent_add_row").click(function(){
      $('#patent_addr'+patent_i).html("<td>"+ (patent_i+1) 
        +"</td><td><input type='text' name='patent_author"+patent_i
        +"' id='patent_author"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='patent_patent"+patent_i
        +"' id='patent_patent"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='patent_publishid"+patent_i
        +"' id='patent_publishid"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='patent_time"+patent_i
        +"' id='patent_time"+patent_i
        +"' class='form-control px100'/>"
        +"</td><td><select name='patent_lastyear"+patent_i
        +"' id='patent_lastyear"+patent_i
        +"' class='form-control px100'/></select></td>");

      $('#patent').append('<tr id="patent_addr'+(patent_i+1)+'"></tr>');
      document.getElementById("patent_lastyear"+patent_i).add(new Option("否","否"))
      document.getElementById("patent_lastyear"+patent_i).add(new Option("是","是"))
      patent_i++; 
  });
     $("#patent_delete_row").click(function(){
       if(patent_i>=1){
     $("#patent_addr"+(patent_i-1)).html('');
     patent_i--;
     }
   });

  var project_i = 0

  $("#project_add_row").click(function(){
      $('#project_addr'+project_i).html("<td>"+ (project_i+1) 
        +"</td><td><input type='text' name='project_author"+project_i
        +"' id='project_author"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='project_project"+project_i
        +"' id='project_project"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='project_time"+project_i
        +"' id='project_time"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><select name='project_type"+project_i
        +"' id='project_type"+project_i
        +"' class='form-control px100'/>"
        +"</td><td><select name='project_lastyear"+project_i
        +"' id='project_lastyear"+project_i
        +"' class='form-control px100'/></select></td>");

      $('#project').append('<tr id="project_addr'+(project_i+1)+'"></tr>');
      document.getElementById("project_type"+project_i).add(new Option("国家级奖励","国家级奖励"))
      document.getElementById("project_type"+project_i).add(new Option("省级部一等奖项目","省级部一等奖项目"))
      document.getElementById("project_type"+project_i).add(new Option("省级部二等奖项目","省级部二等奖项目"))
      document.getElementById("project_lastyear"+project_i).add(new Option("否","否"))
      document.getElementById("project_lastyear"+project_i).add(new Option("是","是"))
      project_i++; 
  });
     $("#project_delete_row").click(function(){
       if(project_i>=1){
     $("#project_addr"+(project_i-1)).html('');
     project_i--;
     }
   });

     var standard_i = 0

  $("#standard_add_row").click(function(){
      $('#standard_addr'+standard_i).html("<td>"+ (standard_i+1) 
        +"</td><td><input type='text' name='standard_author"+standard_i
        +"' id='standard_author"+standard_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='standard_standard"+standard_i
        +"' id='standard_standard"+standard_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='standard_time"+standard_i
        +"' id='standard_time"+standard_i
        +"' class='form-control px100'/>"
        +"</td><td><select name='standard_lastyear"+standard_i
        +"' id='standard_lastyear"+standard_i
        +"' class='form-control px100'/></select></td>");

      $('#standard').append('<tr id="standard_addr'+(standard_i+1)+'"></tr>');
      document.getElementById("standard_lastyear"+standard_i).add(new Option("否","否"))
      document.getElementById("standard_lastyear"+standard_i).add(new Option("是","是"))
      standard_i++; 
  });
     $("#standard_delete_row").click(function(){
       if(standard_i>=1){
     $("#standard_addr"+(standard_i-1)).html('');
     standard_i--;
     }
   });

    var confaward_i = 0

  $("#confaward_add_row").click(function(){
      $('#confaward_addr'+confaward_i).html("<td>"+ (confaward_i+1) 
        +"</td><td><input type='text' name='confaward_author"+confaward_i
        +"' id='confaward_author"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='confaward_confaward"+confaward_i
        +"' id='confaward_confaward"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='confaward_conf"+confaward_i
        +"' id='confaward_conf"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='confaward_CCF"+confaward_i
        +"' id='confaward_CCF"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='confaward_time"+confaward_i
        +"' id='confaward_time"+confaward_i
        +"' class='form-control px100'/>"
        +"</td><td><select name='confaward_lastyear"+confaward_i
        +"' id='confaward_lastyear"+confaward_i
        +"' class='form-control px100'/></select></td>");

      $('#confaward').append('<tr id="confaward_addr'+(confaward_i+1)+'"></tr>');
      document.getElementById("confaward_lastyear"+confaward_i).add(new Option("否","否"))
      document.getElementById("confaward_lastyear"+confaward_i).add(new Option("是","是"))
      confaward_i++; 
  });
     $("#confaward_delete_row").click(function(){
       if(confaward_i>=1){
     $("#confaward_addr"+(confaward_i-1)).html('');
     confaward_i--;
     }
   });

    var job_i = 0

  $("#job_add_row").click(function(){
      $('#job_addr'+job_i).html("<td>"+ (job_i+1) 
        +"</td><td><input type='text' name='job_job"+job_i
        +"' id='job_job"+job_i
        +"' class='form-control px150'/>"
        +"</td><td><select name='job_level"+job_i
        +"' id='job_level"+job_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='job_starttime"+job_i
        +"' id='job_starttime"+job_i
        +"' class='form-control px100'/>"
        +"</td><td><input type='text' name='job_endtime"+job_i
        +"' id='job_endtime"+job_i
        +"' class='form-control px100'/>"
        +"</td><td><input type='text' name='job_months"+job_i
        +"' id='job_months"+job_i
        +"' class='form-control px100'/></td>");

      $('#job').append('<tr id="job_addr'+(job_i+1)+'"></tr>');
      document.getElementById("job_level"+job_i).add(new Option("A","A"))
      document.getElementById("job_level"+job_i).add(new Option("B","B"))
      document.getElementById("job_level"+job_i).add(new Option("C","C"))
      document.getElementById("job_level"+job_i).add(new Option("D","D"))
      job_i++; 
  });
     $("#job_delete_row").click(function(){
       if(job_i>=1){
     $("#job_addr"+(job_i-1)).html('');
     job_i--;
     }
   });

  var accupro_i = 0

  $("#accupro_add_row").click(function(){
      $('#accupro_addr'+accupro_i).html("<td>"+ (accupro_i+1) 
        +"</td><td><select name='accupro_accupro"+accupro_i
        +"' id='accupro_accupro"+accupro_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='accupro_content"+accupro_i
        +"' id='accupro_content"+accupro_i
        +"' class='form-control px150'/>"
        +"</td><td><input type='text' name='accupro_time"+accupro_i
        +"' id='accupro_time"+accupro_i
        +"' class='form-control px100'/></td>");

      $('#accupro').append('<tr id="accupro_addr'+(accupro_i+1)+'"></tr>');
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("A","A"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("B","B"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("C","C"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("D","D"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("E","E"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("F1","F1"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("F2","F2"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("F3","F3"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("G","G"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("H","H"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("I","I"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("J","J"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("K1","K1"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("K2","K2"))
      document.getElementById("accupro_accupro"+accupro_i).add(new Option("K3","K3"))
      accupro_i++; 
  });
     $("#accupro_delete_row").click(function(){
       if(accupro_i>=1){
     $("#accupro_addr"+(accupro_i-1)).html('');
     accupro_i--;
     }
   });

});
