let images = {}
let atlas;
let ready=false;
document.addEventListener("DOMContentLoaded",(event)=>{
    atlas = document.getElementById("atlas");
    atlas.addEventListener("load",(e)=>{
        ready=true;
        setInterval(refreshData,50)
    })
})
function refreshData()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.responseText!="")
        updateData(JSON.parse(this.responseText));
        // console.log(this.responseText);
    };
    xhttp.open("GET", "jsonObj",true)
    xhttp.send();
}
function updateData(data)
{
    // data = document.getElementById("stuff");
    if(ready==false)
        return;
    let canvases = document.getElementsByClassName("players");
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
        displayPlace(data[i].place,currentCanvas,width,height)
        console.log(data[i].place)

    }
}
function displayPlace(num, ctx,width,height)
{
    //draws the image onto passed canvas
    if(num!=-1)
    ctx.drawImage(atlas, 180*(num-1),0, 180, 128, 0, 0, width, height);
}