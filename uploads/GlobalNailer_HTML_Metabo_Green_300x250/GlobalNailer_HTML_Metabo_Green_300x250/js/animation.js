var creative = {}; //ad object

function init() {
    // addEventListeners();
	console.log("Ad Ready");
	creative.viewport = document.getElementById('mainExit');
	gsap.set(['#viewport', '#border', '.init'], {autoAlpha:1});
	// gsap.set(['#temp'], {alpha:0.5});
	frameOne();
	gsap.set("#cta-hover", {autoAlpha:0})
}

function frameOne() {
	var frameDelay = 1.9;
	gsap.set(['.gl', '.f1' ], {autoAlpha:1});

	gsap.from("#f1_txt1", {opacity:0, y:"-=10", ease:"power2.out", ease:"elastic.out(0.1, 0.6)", delay:0.5})
	gsap.from(["#product1"], {x:"+=300", rotation:-10, y:"-=10", ease:"power4.inOut", duration:1})

	gsap.to(["#f1_txt1"], {autoAlpha:0,y:"+=10", ease:"elastic.out(0.1, 0.6)", delay:frameDelay})       
	gsap.delayedCall(frameDelay, frameTwo);
}


function frameTwo() {
	var frameDelay = 1.9;

	gsap.set(['.f2' ], {autoAlpha:1});

	gsap.from("#f2_txt1", {opacity:0, y:"-=10", ease:"power2.out", ease:"elastic.out(0.1, 0.6)", delay:0.5})
	gsap.from(["#product2"], {x:"+=240", rotation:-10, y:"+=30", ease:"power4.inOut", duration:1}, 0.75)
	
	gsap.to(["#f2_txt1"], {autoAlpha:0,y:"+=10", ease:"elastic.out(0.1, 0.6)", delay:frameDelay})       
	gsap.delayedCall(frameDelay, frameThree);
}

function frameThree() {
	var frameDelay = 1.9;

	gsap.set(['.f3' ], {autoAlpha:1});

	gsap.from("#f3_txt1", {opacity:0, y:"-=10", ease:"power2.out", ease:"elastic.out(0.1, 0.6)", delay:0.5})
	gsap.from(["#product3"], {x:"+=240", rotation:-10, y:"+=30", ease:"power4.inOut", duration:1}, 0.75)

	gsap.to(["#f3_txt1"], {autoAlpha:0,y:"+=10", ease:"elastic.out(0.1, 0.6)", delay:frameDelay})       
	gsap.delayedCall(frameDelay, endFrame);
}

function endFrame() {
	gsap.set(['.ef' ], {autoAlpha:1});
    var tl = gsap.timeline();
        tl
	.from("#ef_txt1", {scale:2.5, opacity:0, ease:"power2.out", duration:0.5,  ease:"elastic.out(0.7, 0.6)", delay:0.5, transformOrigin:"150px 190px"})
	.to("#logo", {x:-98, ease:"power2.inOut", delay:2})
	.from("#cta-line", {scaleY:0, ease:"power3.inOut"})
	.from([".cta-logo"], {x:-110, stagger:0.5, autoAlpha:0})
	.to("#cta", {opacity:1, delay:0.4, onComplete:addEvents})

}

// CTA Hover
function addEvents(){ 
    creative.viewport.addEventListener("mouseover", bannerOver)

}
function bannerOver(e){ 
    creative.viewport.addEventListener("mouseout", bannerOut)
    creative.viewport.removeEventListener("mouseover", bannerOver)
	

gsap.to("#cta-hover", {autoAlpha:1, duration:0.3, ease:"power1.out"})
}
function bannerOut(e){
    creative.viewport.removeEventListener("mouseout", bannerOut)
    creative.viewport.addEventListener("mouseover", bannerOver)
	gsap.to("#cta-hover", {autoAlpha:0, duration:0.3, ease:"power1.out"})

}

// Studio Exit Handlers (ClickTags)
// function addEventListeners() { 
//     function mainExitHandler(e) { Enabler.exit('MainExit'); }
//     document.getElementById('mainExit').addEventListener('click', mainExitHandler, false);
// }