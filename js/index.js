var setIframe = function(id) {
  var Iframe = document.getElementById(id);
  try {
    // 声明变量取值
    var bHeight = Iframe.contentWindow.document.body.scrollHeight;
    var dHeight = Iframe.contentWindow.document.documentElement.scrollHeight;
    var height = Math.max(bHeight, dHeight); // 取最大值
    Iframe.height = height;
  } catch (ex) { }
};

var sidearrayleft  = new Vue({
  el:'#side-arrays-left',
  data:{
    items:[
    {"id": 0,"title": "HTML教程","href": "./content/codef.htm"},
    {"id": 0,"title": "HTML教程tttt","href": "ContentCollect/ok.html"}
  ]
  },
  created:function(){
    //this.getJson();
  },
  methods:{
    getJson: function(){
      const url = "http://va.fyping.cn:63480/example";
      this.$http.get(url).then(Response =>{
        console.log(Response.body);
        this.items = Response.body;
      },err =>{
        console.log(err);
      }) 
    },
    hello:function(event){
      var iifattr = {
                    id:"main-content-iframe",
                    height:"100%",
                    width:"100%",
                    scrolling:"yes",
                    frameborder:"0"
                    }
      var el = event.currentTarget;
      var href = el.getAttribute('conthref');
      iifattr['src']=href;
      var content_head_info = document.createElement("div");
      content_head_info.setAttribute("class","demand-info");

      var idd = el.getAttribute("id");
      idd = idd.substr(9,idd.length);
      
      var ffflag = "";
      var sssasrc = "/";
      idd=idd*1;
      if(idd==0){
        ffflag = "首页";
      }else if (idd==idd.length){

      }else{
        var true_id = idd*1 -1;
        var its = document.getElementById("side-bar-"+true_id);
        ffflag = its.innerText;
      }
      var last_content = document.createTextNode(ffflag);
      var ddls = document.createElement("div");
      var sssp = document.createElement("span");
      var sssa = document.createElement("a");

      sssa.setAttribute("src",sssasrc);
      sssp.append(last_content);
      sssa.append(sssp);
      ddls.setAttribute("class","ddls-cont");
      ddls.append(sssa);

      content_head_info.append(ddls);
      var iframe = document.createElement("iframe");
      for( var i in iifattr){
        iframe.setAttribute(i,iifattr[i]);  
      }
      var eee = document.getElementById("main-content");
      if(eee.childElementCount==2){
          eee.replaceChild(content_head_info,eee.children[0]);
          eee.replaceChild(iframe,eee.children[1]);
      }else{
        eee.append(content_head_info);
        eee.append(iframe);
      }
      window.setInterval("setIframe('main-content-iframe')",10);
    }
  }
});



//window.setInterval("setiframe('right_iframe')", 10);   //0.01秒周期调用函数
