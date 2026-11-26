// PACP procedural 3D brain: independently rendered WebGL geometry, not a video or cropped image.
// Three.js is loaded only for the enhancement; the original visual remains as a graceful fallback.
const stage=document.getElementById('brainStage');
const art=document.getElementById('heroArt');
const status=document.getElementById('renderStatus');
const toggle=document.getElementById('motionToggle');
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
let moving=!reduce.matches, sceneReady=false;
if(!moving){toggle.setAttribute('aria-pressed','false');toggle.textContent='تشغيل حركة المشهد';}
toggle.addEventListener('click',()=>{moving=!moving;toggle.setAttribute('aria-pressed',String(moving));toggle.textContent=moving?'إيقاف حركة المشهد':'تشغيل حركة المشهد';});
function canWebGL(){try{const c=document.createElement('canvas');return !!(c.getContext('webgl2')||c.getContext('webgl'));}catch{return false;}}
if(!canWebGL()){status.textContent='الجهاز لا يدعم WebGL؛ يظهر البديل البصري.';}
else {
 try {
  const THREE=await import('https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js');
  const canvas=document.getElementById('brainCanvas');
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.7));
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(34,1,.1,100);camera.position.set(0,0,11.5);
  scene.add(new THREE.AmbientLight(0xa7fff0,1.2));
  const light=new THREE.PointLight(0x7bffda,100,20);light.position.set(-3,4,6);scene.add(light);
  const rim=new THREE.PointLight(0x42baff,80,18);rim.position.set(3,-2,-2);scene.add(rim);
  const root=new THREE.Group();scene.add(root);
  const shell=new THREE.MeshPhysicalMaterial({color:0x22c8b3,metalness:.22,roughness:.16,transmission:.35,thickness:1,transparent:true,opacity:.72,side:THREE.DoubleSide,depthWrite:false});
  const grooves=new THREE.MeshBasicMaterial({color:0xc7fff3,transparent:true,opacity:.75});
  const neurons=new THREE.MeshBasicMaterial({color:0xaaffea});
  // Two deformed cerebral hemispheres with parametric gyri and sulci.
  function lobe(side){
    const geo=new THREE.SphereGeometry(1,64,48),pos=geo.attributes.position,v=new THREE.Vector3();
    for(let i=0;i<pos.count;i++){
      v.fromBufferAttribute(pos,i);
      const wave=.055*Math.sin(v.y*21+Math.sin(v.x*8)*3)*Math.cos(v.z*16)+.035*Math.sin(v.x*29+v.y*11);
      const x=v.x*(1+wave)*1.34,y=v.y*(1+wave)*1.07,z=v.z*(1+wave)*.83;
      pos.setXYZ(i,x+side*.93,y+.45,z);
    }
    geo.computeVertexNormals();root.add(new THREE.Mesh(geo,shell));
    for(let j=0;j<19;j++){
      const pts=[];const phi=.23+j*.155;
      for(let k=0;k<=90;k++){
        const t=k/90*Math.PI*2;
        const r=1.018+.045*Math.sin(t*8+j*1.4)+.025*Math.cos(t*15+j);
        pts.push(new THREE.Vector3(side*.93+1.34*r*Math.sin(phi)*Math.cos(t),.45+1.07*r*Math.cos(phi),.83*r*Math.sin(phi)*Math.sin(t)));
      }
      const curve=new THREE.CatmullRomCurve3(pts);
      root.add(new THREE.Mesh(new THREE.TubeGeometry(curve,90,.007,4,false),grooves));
    }
  }
  lobe(-1);lobe(1);
  // Brainstem and cerebellum.
  const stem=new THREE.Mesh(new THREE.CylinderGeometry(.21,.15,1.45,24),shell);stem.position.set(0,-1.62,0);stem.rotation.z=.15;root.add(stem);
  const cerebellum=new THREE.Mesh(new THREE.SphereGeometry(.76,32,24),shell);cerebellum.scale.set(1.1,.48,.66);cerebellum.position.set(.45,-.85,-.15);root.add(cerebellum);
  // Independently animated neural points and connective arcs.
  const positions=[];const seeds=[];
  for(let i=0;i<100;i++){
    const a=i*2.399963229728653, z=1-2*(i+.5)/100, r=Math.sqrt(1-z*z), x=r*Math.cos(a),y=z,zz=r*Math.sin(a);
    const side=x<0?-1:1;
    const p=new THREE.Vector3(side*.93+x*1.34,y*1.08+.45,zz*.86);
    positions.push(p);seeds.push(i);
    const bead=new THREE.Mesh(new THREE.SphereGeometry(i%7===0?.043:.023,7,7),neurons);bead.position.copy(p);root.add(bead);
  }
  const lineMat=new THREE.LineBasicMaterial({color:0x74ffe0,transparent:true,opacity:.28,depthWrite:false});
  for(let i=0;i<positions.length;i++){
    for(let j=i+1;j<positions.length;j++){
      if(positions[i].distanceTo(positions[j])<.59 && (i+j)%3===0){
        const g=new THREE.BufferGeometry().setFromPoints([positions[i],positions[j]]);
        root.add(new THREE.Line(g,lineMat));
      }
    }
  }
  const ringMat=new THREE.MeshBasicMaterial({color:0x00ad7d,transparent:true,opacity:.5,side:THREE.DoubleSide});
  for(let i=0;i<3;i++){
    const ring=new THREE.Mesh(new THREE.TorusGeometry(2.4+i*.19,.012,6,120),ringMat);
    ring.rotation.x=Math.PI/2.7;ring.position.y=-2.34-i*.07;root.add(ring);
  }
  const glyph=document.createElement('div');glyph.textContent='Ψ';glyph.setAttribute('aria-hidden','true');
  Object.assign(glyph.style,{position:'absolute',left:'50%',top:'49%',transform:'translate(-50%,-50%)',font:'bold 90px Georgia,serif',color:'#d7ffe6',textShadow:'0 0 10px #8dffdb,0 0 28px #1dff8c',pointerEvents:'none'});stage.append(glyph);
  function resize(){const w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}
  resize();new ResizeObserver(resize).observe(stage);
  let targetX=0,targetY=0,rx=0,ry=0,clock=0;
  stage.addEventListener('pointermove',e=>{if(!moving)return;const r=stage.getBoundingClientRect();targetY=((e.clientX-r.left)/r.width-.5)*.35;targetX=((e.clientY-r.top)/r.height-.5)*.22;});
  stage.addEventListener('pointerleave',()=>{targetX=targetY=0;});
  let visible=true;new IntersectionObserver(entries=>visible=entries[0]?.isIntersecting??true).observe(stage);
  function frame(){requestAnimationFrame(frame);if(!visible||document.hidden)return;if(moving){clock+=.007;rx+=(targetX-rx)*.05;ry+=(targetY-ry)*.05;root.rotation.set(rx+Math.sin(clock*.65)*.025,ry+Math.sin(clock)*.09,0);root.position.y=Math.sin(clock*1.4)*.07;}renderer.render(scene,camera);}
  frame();stage.classList.add('ready');art.classList.add('webgl-ready');sceneReady=true;
  status.textContent='مشهد WebGL ثلاثي الأبعاد فعلي — حرّك المؤشر لاستكشافه';
 }catch(error){console.warn('PACP 3D fallback:',error);status.textContent='يتطلب المشهد ثلاثي الأبعاد اتصالًا بالإنترنت؛ تظهر الصورة المرجعية بدلًا منه.';}
}
