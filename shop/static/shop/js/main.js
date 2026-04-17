// Cursor
const c1=document.getElementById('cur'),c2=document.getElementById('cur2');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;});
(function loop(){
  c1.style.left=mx+'px';c1.style.top=my+'px';
  rx+=(mx-rx)*.12;ry+=(my-ry)*.12;
  c2.style.left=rx+'px';c2.style.top=ry+'px';
  requestAnimationFrame(loop);
})();
document.querySelectorAll('a,button').forEach(el=>{
  el.addEventListener('mouseenter',()=>document.body.classList.add('ha'));
  el.addEventListener('mouseleave',()=>document.body.classList.remove('ha'));
});

// Scroll reveal
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in');});},{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// FAQ
function faq(btn){
  const ans=btn.nextElementSibling,open=btn.classList.contains('open');
  document.querySelectorAll('.faq-q').forEach(b=>{b.classList.remove('open');b.nextElementSibling.classList.remove('open');});
  if(!open){btn.classList.add('open');ans.classList.add('open');}
}

// Ensure FAQ is global if needed
window.faq = faq;
