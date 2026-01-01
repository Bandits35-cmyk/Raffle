const ADMIN_KEY = "supersecret123"; // SAME AS RENDER

function spin() {
  if (spinning) return;
  spinning = true;

  const duration = Math.random()*2000 + 3000;
  let start = null;

  function anim(t){
    if(!start) start = t;
    angle += 0.15;
    draw();
    if(t-start < duration){
      requestAnimationFrame(anim);
    } else {
      spinning = false;
      announce();
    }
  }
  requestAnimationFrame(anim);
}

function announce(){
  fetch("https://YOUR-RENDER-URL.onrender.com/spin",{
    method:"POST",
    headers:{
      "X-ADMIN-KEY": ADMIN_KEY
    }
  })
  .then(r=>r.json())
  .then(d=>{
    alert("🎉 WINNER: @" + d.winner);
  });
}
