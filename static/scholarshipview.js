function getscores(username){
  $.ajax({
      type:"POST",
      url:"/getscores/"+username,
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)

          infolist = ['accupro','academic','standard','project','shegong','conf','qikan','patent','job']
      for (i in infolist){

              info = infolist[i]
              document.getElementById(info+"score").innerHTML=parseInt(1000*result[info])/1000
      }
      }
    })
}


function getotherscholarshipinfo(username){
  
      d = {}
      d['userid'] = getCookie('useridthu')
      d['username'] = getCookie('usernamethu')
      d['token'] = getCookie('tokenthu')
      
      $.ajax({
      type:"POST",
      url:"/getscholarshipinfo/"+username,
      data: d,
      success:function userinfo_return(data){
        result = JSON.parse(data)
        if (result['success'] == 1){
          result = JSON.parse(result['scholarshipinfo'])
          //inputinfo
          infolist = ['name','class','sex','school_roll','political','grade','suo'
          ,'ethnic','mas_doc','mentor','email','mobile','kaiti','tice',
          'otheraward', 'username']
          for (i=0;i<infolist.length;i++){
            info = infolist[i]
            //if (result.has_key(info)){
              document.getElementById(info).value=result[info]
            //}
          }
          //tableinfo
          infolist=['conf','qikan','patent','project','standard','confaward','job','accupro']
          infosublist=[['author','yizuo','CCF','conf','paper','time','pages', 'papertype','lastyear'],
          ['author','yizuo','CCF','qikan','paper','time','pagenum','pages', 'papertype','lastyear'],
          ['author','yizuo','patent','publishid','time','lastyear'],
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
                if ((sublist[1] == 'yizuo') && !(result[info+"_"+sublist[1]+num])){
                  document.getElementById(info+"_"+sublist[1]+num).value='是'
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
        +"</td><td><input readOnly type='text' name='conf_author"+conf_i
        +"' id='conf_author"+conf_i
        +"' class='form-control px150'/> </td><td><input readOnly type='text' name='conf_yizuo"+conf_i
        +"' id='conf_yizuo"+conf_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='conf_CCF"+conf_i
        +"' id='conf_CCF"+conf_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='conf_conf"+conf_i
        +"' id='conf_conf"+conf_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='conf_paper"+conf_i
        +"' id='conf_paper"+conf_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='conf_time"+conf_i
        +"' id='conf_time"+conf_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='conf_pages"+conf_i
        +"' id='conf_pages"+conf_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='conf_papertype"+conf_i
        +"' id='conf_papertype"+conf_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='conf_lastyear"+conf_i
        +"' id='conf_lastyear"+conf_i
        +"' class='form-control px100'/></td>");

      $('#conf').append('<tr id="conf_addr'+(conf_i+1)+'"></tr>');
      
      
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
        +"</td><td><input readOnly type='text' name='qikan_author"+qikan_i
        +"' id='qikan_author"+qikan_i
        +"' class='form-control px150'/> </td><td><input readOnly type='text' name='qikan_yizuo"+qikan_i
        +"' id='qikan_yizuo"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='qikan_CCF"+qikan_i
        +"' id='qikan_CCF"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='qikan_qikan"+qikan_i
        +"' id='qikan_qikan"+qikan_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='qikan_paper"+qikan_i
        +"' id='qikan_paper"+qikan_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='qikan_time"+qikan_i
        +"' id='qikan_time"+qikan_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='qikan_pagenum"+qikan_i
        +"' id='qikan_pagenum"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='qikan_pages"+qikan_i
        +"' id='qikan_pages"+qikan_i
        +"' class='form-control px50'/>"
        +"</td><td><input readOnly type='text' name='qikan_papertype"+qikan_i
        +"' id='qikan_papertype"+qikan_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='qikan_lastyear"+qikan_i
        +"' id='qikan_lastyear"+qikan_i
        +"' class='form-control px100'/></td>");

      $('#qikan').append('<tr id="qikan_addr'+(qikan_i+1)+'"></tr>');

      
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
        +"</td><td><input readOnly type='text' name='patent_author"+patent_i
        +"' id='patent_author"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='patent_yizuo"+patent_i
        +"' id='patent_yizuo"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='patent_patent"+patent_i
        +"' id='patent_patent"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='patent_publishid"+patent_i
        +"' id='patent_publishid"+patent_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='patent_time"+patent_i
        +"' id='patent_time"+patent_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='patent_lastyear"+patent_i
        +"' id='patent_lastyear"+patent_i
        +"' class='form-control px100'/></td>");

      $('#patent').append('<tr id="patent_addr'+(patent_i+1)+'"></tr>');
      
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
        +"</td><td><input readOnly type='text' name='project_author"+project_i
        +"' id='project_author"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='project_project"+project_i
        +"' id='project_project"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='project_time"+project_i
        +"' id='project_time"+project_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='project_type"+project_i
        +"' id='project_type"+project_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='project_lastyear"+project_i
        +"' id='project_lastyear"+project_i
        +"' class='form-control px100'/></td>");

      $('#project').append('<tr id="project_addr'+(project_i+1)+'"></tr>');
      
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
        +"</td><td><input readOnly type='text' name='standard_author"+standard_i
        +"' id='standard_author"+standard_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='standard_standard"+standard_i
        +"' id='standard_standard"+standard_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='standard_time"+standard_i
        +"' id='standard_time"+standard_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='standard_lastyear"+standard_i
        +"' id='standard_lastyear"+standard_i
        +"' class='form-control px100'/></td>");

      $('#standard').append('<tr id="standard_addr'+(standard_i+1)+'"></tr>');

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
        +"</td><td><input readOnly type='text' name='confaward_author"+confaward_i
        +"' id='confaward_author"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='confaward_confaward"+confaward_i
        +"' id='confaward_confaward"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='confaward_conf"+confaward_i
        +"' id='confaward_conf"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='confaward_CCF"+confaward_i
        +"' id='confaward_CCF"+confaward_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='confaward_time"+confaward_i
        +"' id='confaward_time"+confaward_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='confaward_lastyear"+confaward_i
        +"' id='confaward_lastyear"+confaward_i
        +"' class='form-control px100'/></td>");

      $('#confaward').append('<tr id="confaward_addr'+(confaward_i+1)+'"></tr>');
     
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
        +"</td><td><input readOnly type='text' name='job_job"+job_i
        +"' id='job_job"+job_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='job_level"+job_i
        +"' id='job_level"+job_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='job_starttime"+job_i
        +"' id='job_starttime"+job_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='job_endtime"+job_i
        +"' id='job_endtime"+job_i
        +"' class='form-control px100'/>"
        +"</td><td><input readOnly type='text' name='job_months"+job_i
        +"' id='job_months"+job_i
        +"' class='form-control px100'/></td>");

      $('#job').append('<tr id="job_addr'+(job_i+1)+'"></tr>');

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
        +"</td><td><input readOnly type='text' name='accupro_accupro"+accupro_i
        +"' id='accupro_accupro"+accupro_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='accupro_content"+accupro_i
        +"' id='accupro_content"+accupro_i
        +"' class='form-control px150'/>"
        +"</td><td><input readOnly type='text' name='accupro_time"+accupro_i
        +"' id='accupro_time"+accupro_i
        +"' class='form-control px100'/></td>");

      $('#accupro').append('<tr id="accupro_addr'+(accupro_i+1)+'"></tr>');
      
      accupro_i++; 
  });
     $("#accupro_delete_row").click(function(){
       if(accupro_i>=1){
     $("#accupro_addr"+(accupro_i-1)).html('');
     accupro_i--;
     }
   });

});
