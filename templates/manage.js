let cameras;
let currentImage;
let obsMode = false;
document.addEventListener("DOMContentLoaded",(event)=>{
    obsMode = '{{ obsMode }}'=='True'
    setActivity("DisableOBSMode",obsMode)
    setClassActivity("videoManage",'{{ readingData }}'=='True')
    setActivity("start",'{{ readingData }}'=='False')
    retrieveCams()
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
            setCamForm()
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
    setCameras()
    // let xhttp = new XMLHttpRequest();
    // xhttp.open("GET","start",true);
    // xhttp.send()
}
function stopReading()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","stop",true);
    xhttp.send()
    for(el of document.getElementsByClassName("videoManage"))
        setActivity(el,false)
    setClassActivity("obsManage",true)
    setActivity(document.getElementById("start"),true)
}
function setClassActivity(className, status)
{
    for(el of document.getElementsByClassName(className))
        setActivity(el,status)
}
function setActivity(element, status)
{
    if(typeof(element)==typeof(""))
    {
        element = document.getElementById(element)
    }
    if(status)
    {
        element.classList.add("active")
        element.classList.remove("inactive")
    }
    else
    {
    element.classList.add("inactive")
    element.classList.remove("active")
    }
}
function toggleOrder()
{
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET","toggleOrder",true);
    xhttp.send()
}
function setCamForm()
{
    document.getElementById("cameraList").textContent=""
    loopCamsToForm(0,cameras.length)
}
function loopCamsToForm(index,maxLength)
{
    if(index>=maxLength)
        return 0
    let i = index
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
        if(this.readyState==4 && this.status == 200)
        {
            addCamToForm(index, this.responseText)
            return loopCamsToForm(index+1,maxLength)
        }
    }
    xhttp.open("GET","camImage/"+cameras[i],true)
    xhttp.send()
}
function addCamToForm(index, image)
{
    let i = index
    let doc = document.getElementById("cameraList")
    let imageDoc = document.createElement("img")
    imageDoc.width=1280;
    imageDoc.height=720;
    imageDoc.src="data:image/png;base64," + image
    let comboDoc= document.createElement("div")
    let indexDoc= document.createElement("p")
    let inputDoc= document.createElement("input")
    inputDoc.type="text";
    inputDoc.className="nameField"
    let ordDoc= document.createElement("input")
    ordDoc.type="number";
    ordDoc.className="orderBox"
    ordDoc.style.display="none"
    let setVirtCam = document.createElement("meta")
    if(!obsMode){
        setVirtCam = document.createElement("input")
        setVirtCam.className ="obsManage"
        setVirtCam.type="button"
        setVirtCam.textContent="Set OBS Virtual Camera";
        setVirtCam.addEventListener('click',function(){
            setOBScam(i)
        })
    }
        
    indexDoc.textContent = i;
    comboDoc.appendChild(indexDoc);
    comboDoc.appendChild(imageDoc);
    comboDoc.appendChild(inputDoc);
    comboDoc.appendChild(ordDoc);
    comboDoc.appendChild(setVirtCam)
    doc.appendChild(comboDoc)
}
function disableOBS()
{
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function()
    {
        if(xhttp.readyState==4 && xhttp.status==200)
        {
            document.getElementById("DisableOBSMode").classList.add("inactive")
            document.getElementById("DisableOBSMode").classList.remove("active")
            console.log("OBS Mode Disabled")
            obsMode = false
            retrieveCams()

        }
    }
    xhttp.open("GET","disableOBS",true)
    xhttp.send()
}
function setOBScam(index)
{
    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function()
    {
        if(xhttp.readyState==4 && xhttp.status==200)
        {
            document.getElementById("DisableOBSMode").classList.add("active")
            document.getElementById("DisableOBSMode").classList.remove("inactive")
            console.log("OBS Virt Cam Accepted")
            obsMode=true
            retrieveCams()
        }
    }
    xhttp.open("POST","sendOBS", true);
    xhttp.send(index);
}
function setCameras()
{
    if(document.getElementById("cameraList").length==0)
        setCamForm();
    let doc = document.getElementsByClassName("nameField")
    let ord = document.getElementsByClassName("orderBox")
    let playerList = []
    console.log(doc)
    
    for(let i = 0; i < doc.length; i++)
    {
        if(doc[i].value!="")
        {
            console.log("checking Data")
            let currentOrd = ord[i].value
            if(currentOrd == "")
                {
                    currentOrd=-1
                }
                playerList.push([cameras[i],doc[i].value,currentOrd]);
        }
    }

    let xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function()
    {
        if(xhttp.readyState==4 && xhttp.status==200)
        {
            console.log("Camera Data Accepted")
            let xhttp = new XMLHttpRequest();
            xhttp.open("GET","start",true);
            xhttp.send()
            setActivity(document.getElementById("start"),false)
            setClassActivity("obsManage",false)
            for(el of document.getElementsByClassName("videoManage"))
            {
                el.classList.remove("inactive")
                el.classList.add("active")
            }
        }
    }
    xhttp.open("POST","sendCams", true);
    console.log(playerList);
    xhttp.send(JSON.stringify(playerList));
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