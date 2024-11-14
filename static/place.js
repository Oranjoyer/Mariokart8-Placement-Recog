let images = {}
let atlasB;
let atlasWhite;
let atlasRed;
let atlasBlue;
let flag;
let ready=false;
let firstTime = true;
let url = window.page;
let externalData;
document.addEventListener("DOMContentLoaded",(event)=>{
    externalData = JSON.parse(document.getElementById("externalData").getAttribute("data"));
    if(externalData.type!="name")
    {
        atlasB = document.getElementById("atlasBack");
        atlasRed = document.getElementById("atlasRed");
        atlasBlue = document.getElementById("atlasBlue");
        atlasWhite = document.getElementById("atlasWhite");
        flag = document.getElementById("flag")
    }
    // console.log(document.getElementById("externalData").getAttribute("data"));
    if(externalData.type!="name")
    {
        atlasWhite.addEventListener("load",(e)=>{
            ready=true;
            setInterval(refreshData,500)
        })
    }
    else
    {
        ready=true;
        setInterval(refreshData,1000);
    }
})
function refreshData()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState==4&&this.status==200&&this.responseText!="")
        updateData(JSON.parse(this.responseText));
        // console.log(this.responseText);
    };
    xhttp.open("GET", "jsonObj",true)
    xhttp.send();
}
function updateData(data)
{
    let pageType=externalData.type
    let camNum=externalData.number
    if(camNum!=-1)
    {
        data=[data[camNum]]
    }
    // console.log("Length of Data: "+data.length)
    if(firstTime||document.getElementsByClassName("player").length!=data.length)
    {
        document.getElementById("playerList").textContent=""
        // console.log("Setting Stuff")
        for(player of data)
        {
            let doc = document.createElement("div");
            doc.className = "player";
            if(pageType!="name")
            {
                let canvas = document.createElement("canvas")
                canvas.className = "playerCanvas";
                doc.appendChild(canvas)
                // console.log("got here")
            }
            if(pageType!="place")
            {
                let name = document.createElement("p")
                name.textContent = player.name
                name.classList=["playerName"];
                if(pageType!="name")
                    name.classList.add("nameText")
                doc.appendChild(name)
            }
            document.getElementById("playerList").appendChild(doc);
        }
    }
    firstTime = false;
    // data = document.getElementById("stuff");
    if(ready==false||pageType=="name")
        return;
    let canvases = document.getElementsByClassName("playerCanvas");
    // console.log(canvases)
    // console.log(data)
    for (let i = 0; i < canvases.length;i++)
    {
        // console.log(data[i])
        // if(images[data[i].name]==null)
        // {
        //     images[data[i].name] = new Image();
        //     images[data[i].name].src = data[i].name+".jpg";
        // }
        let currentCanvas = canvases[i];
        let height = currentCanvas.height;
        let width = currentCanvas.width;
        currentCanvas = currentCanvas.getContext("2d");
        currentCanvas.clearRect(0,0,width,height);
        displayPlace(data[i].place,currentCanvas,width,height,data[i].team)
        // console.log(data[i].place)
        if(data[i].finished)
            currentCanvas.drawImage(flag,width-48,0,48,48);

    }
}
function displayPlace(num, ctx,width,height,color)
{
    //draws the image onto passed canvas
    if(num==0)
        return
    let teamColor;
    if(color=="Red")
    teamColor=atlasRed;
    else if(color=="Blue")
    teamColor=atlasBlue;
    else
    teamColor=atlasWhite;
    ctx.drawImage(atlasB, 180*(num-1),0, 180, 128, 0, 0, width, height);
    ctx.drawImage(teamColor, 180*(num-1),0, 180, 128, 0, 0, width, height);
    delete teamColor;
}