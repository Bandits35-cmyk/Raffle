const API_BASE_URL = "https://raffle-o573.onrender.com";
const ADMIN_KEY = "supersecret123"; // same sa env

const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");
let users = [], angle=0, spinning=false;

function resize(){
    const size = Math.min(innerWidth, innerHeight)*0.9;
    canvas.width = size; canvas.height = size;
}
resize();
window.onresize = resize;

fetch(`${API_BASE_URL}/participants`)
.then(r=>r.json())
.then(d=>{users=d; draw();});

function color(i){ return `hsl(${i*360/users.length},70%,55%)`; }

function draw(){
    const r = canvas.width/2;
    const step = 2*Math.PI/users.length;
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.save(); ctx.translate(r,r);

    users.forEach((u,i)=>{
        ctx.beginPath();
        ctx.fillStyle = color(i);
        ctx.moveTo(0,0);
        ctx.arc(0,0,r,step*i+angle,step*(i+1)+angle);
        ctx.fill();

        ctx.save();
        ctx.rotate(step*i + step/2 + angle);
        ctx.fillStyle="#fff";
        ctx.font="bold 14px sans-serif";
        ctx.textAlign="right";
        ctx.fillText("@"+u, r-20,5);
        ctx.restore();
    });
    ctx.restore();
}

function spin(){
    if(spinning || users.length===0) return;
    spinning=true;
    const duration=Math.random()*2000+3000;
    let start=null;
    function anim(t){
        if(!start) start=t;
        angle+=0.15; draw();
        if(t-start<duration) requestAnimationFrame(anim);
        else { spinning=false; announce(); }
    }
    requestAnimationFrame(anim);
}

function announce(){
    fetch(`${API_BASE_URL}/spin`,{
        method:"POST",
        headers: { "X-ADMIN-KEY": ADMIN_KEY }
    })
    .then(r=>r.json())
    .then(d=>{
        alert("🎉 WINNER: @" + d.winner);
    });
}
