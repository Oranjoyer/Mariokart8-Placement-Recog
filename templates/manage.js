let cameras;
let currentImage;
document.addEventListener("DOMContentLoaded",(event)=>{
    retrieveCams()
    setCamForm()
})
function retrieveCams()
{
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState==4 && this.status==200)
        {
            cameras = JSON.parse(this.responseText);
            console.log("cameras Gotten")
            console.log(cameras)
        }
    }
    xhttp.open("GET","camList",true);
    xhttp.send()
}
function putInRace()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","inRace",true);
    xhttp.send();
}
function setRed()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","team/Red",true);
    xhttp.send();
}
function setBlue()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","team/Blue",true);
    xhttp.send();
}
function setNone()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","team/White",true);
    xhttp.send();
}
function startReading()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","start",true);
    xhttp.send()
}
function stopReading()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","stop",true);
    xhttp.send()
}
function setCamForm()
{
    document.getElementById("cameraList").textContent=""
    retrieveCams()
    for(let i =0; i< cameras.length;i++)
    {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
        if(this.readyState==4 && this.status == 200)
        {
            let doc = document.getElementById("cameraList")
            let imageDoc = document.createElement("img")
            imageDoc.src="data:image/png;base64," + this.responseText
            let comboDoc= document.createElement("div")
            let indexDoc= document.createElement("p")
            let inputDoc= document.createElement("input")
            inputDoc.type="text";
            inputDoc.className="nameField"
            indexDoc.textContent = i;
            comboDoc.appendChild(indexDoc);
            comboDoc.appendChild(imageDoc);
            comboDoc.appendChild(inputDoc);
            doc.appendChild(comboDoc)
        }
    }
    xhttp.open("GET","camImage/"+cameras[i],true)
    xhttp.send()
    }
}
function setCameras()
{
    if(document.getElementById("cameraList").length==0)
        setCamForm();
    let doc = document.getElementsByClassName("nameField")
    let playerList = []
    console.log(doc)
    
    for(let i = 0; i < doc.length; i++)
    {
        if(doc[i].value!="")
        {
            console.log("checking Data")
            playerList.push([cameras[i],doc[i].value])
        }
    }
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function()
    {
        if(xhttp.readyState==4 && xhttp.status==200)
        {
            console.log("Camera Data Accepted")
        }
    }
    xhttp.open("GET","sendCams/"+JSON.stringify(playerList), true);
    xhttp.send();
}
// function getImage(camera)
// {
//     let screenImg
//     let xhttp = new XMLHttpRequest();
//     xhttp.onreadystatechange = function()
//     {
//         if(this.readyState==4 && this.status == 200)
//         {
//             currentImage = this.responseText
            
//         }
//         // else 
//         // {
//         //     console.log("Image Grab Failed")
//         //     console.log(this.responseText)
//         //     return null
//         // }
//     }
//     xhttp.open("GET","camImage/"+camera,true)
//     xhttp.send()
// }