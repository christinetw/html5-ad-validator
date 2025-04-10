var creative = {}; //ad object

function init() {
    console.log("Ad Ready");
    creative.viewport = document.getElementById('viewport');
    gsap.set(['#viewport', '#border'], {autoAlpha:1});
    // gsap.set(['#tmp'], {autoAlpha:0.5});
    frameOne();
}

function frameOne() {
    gsap.set([".f1", "#logo"], {autoAlpha:1})
    gsap.set(["#counter"], {scale:0.95})


    gsap.from(".f1", {x:"+=0", autoAlpha:0, stagger:0.1, duration:0.9})

    gsap.to(".f1", { autoAlpha:0, delay:4.25})
	gsap.delayedCall(4.75, frameTwo);  
}

function frameTwo() {
    gsap.set([".f2"], {autoAlpha:1})

    gsap.from("#f2-copy", {x:"+=5", autoAlpha:0, duration:0.9})
    gsap.from(["#subject-f2", "#f2-name"], {x:"+=5", autoAlpha:0, delay:0.6, duration:0.9})

    gsap.to(".f2", { autoAlpha:0, delay:3})
	gsap.delayedCall(3.5, endFrame);
}

function endFrame() {
    gsap.set([".ef"], {autoAlpha:1})
    gsap.set("#ef-cta", {transformOrigin:"19% 48%"})
    
    gsap.from("#ef-copy", {x:"+=5", autoAlpha:0, duration:0.9, onComplete:addEventListeners})
    gsap.from(["#subject-ef", "#ef-name"], {x:"+=5", autoAlpha:0, delay:0.6, duration:0.9})

    gsap.to("#ef-cta", {scale:1.12, yoyo:true, repeat:1, duration:0.3, transformOrigin:"368px 60px", delay:1.4})
}

function addEventListeners() {
    creative.viewport.addEventListener("mouseover", bannerOver)
}

function bannerOver(e){
    creative.viewport.removeEventListener("mouseover", bannerOver)
    creative.viewport.addEventListener("mouseout", bannerOut)
    gsap.to(['#ef-cta'],{autoAlpha:0.5, duration:0.1});
}

function bannerOut(e){
    creative.viewport.addEventListener("mouseover", bannerOver)
    creative.viewport.removeEventListener("mouseout", bannerOut)
    gsap.to(['#ef-cta'],{autoAlpha:1, duration:0.1});
}