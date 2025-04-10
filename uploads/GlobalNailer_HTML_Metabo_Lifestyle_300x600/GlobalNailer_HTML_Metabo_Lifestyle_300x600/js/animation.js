var creative = {}; //ad object

function init() {
    // addEventListeners();
	console.log("Ad Ready");
	creative.viewport = document.getElementById('mainExit');
	gsap.set(['#viewport', '#border', '.init'], {autoAlpha:1});
	// gsap.set(['#tmp'], {alpha:0.5});
	frameOne();
	gsap.set("#cta-hover", {autoAlpha:0})

}

function frameOne() {
	var frameDelay = 2;

	gsap.set([ '.gl', '.f1' ], {autoAlpha:1});
    var tl = gsap.timeline();
        tl
	.from("#f1_txt1", {scale:2.5, opacity:0, duration:0.5,  ease:"elastic.out(0.7, 0.6)", transformOrigin:"50% 400px"})


	gsap.to(["#f1_txt1"], {autoAlpha:0, delay:frameDelay})       
	gsap.delayedCall(frameDelay, frameTwo);
}

function frameTwo() {
	var frameDelay = 3;
	gsap.set([ '.f2' ], {autoAlpha:1});
    var tl = gsap.timeline();
        tl
	.to(["#product1","#product2"], {x:"-=300", ease:"power2.inOut", duration:0.8})
	.from("#f2_txt1", {scale:2.5, opacity:0, duration:0.5,  ease:"elastic.out(0.7, 0.6)", transformOrigin:"50% 400px"})

	gsap.to(["#f2_txt1"], {autoAlpha:0, delay:frameDelay})       
	gsap.delayedCall(frameDelay, frameThree);
}

function frameThree() {
	var frameDelay = 3;
	gsap.set([ '.f3' ], {autoAlpha:1});
    var tl = gsap.timeline();
        tl
	.to(["#product2"], {x:"-=300", ease:"power2.inOut", duration:0.8})
	.to(["#product3"], {x:"-=300", ease:"power2.inOut", duration:0.8},'<')
	.from("#f3_txt1", {scale:2.5, opacity:0, duration:0.5,  ease:"elastic.out(0.7, 0.6)", transformOrigin:"50% 400px"})

	gsap.to(["#f3_txt1"], {autoAlpha:0, delay:frameDelay})       
	gsap.delayedCall(frameDelay, endFrame);
}

function endFrame() {
	gsap.set(['.ef' ], {autoAlpha:1});
    var tl = gsap.timeline();
        tl
		.to(["#product3"], {x:"-=300", ease:"power2.inOut", duration:0.8})
		.to(["#product4"], {x:"-=300", ease:"power2.inOut", duration:0.8},'<')
		.from("#ef_txt1", {scale:2.5, opacity:0, duration:0.5,  ease:"elastic.out(0.7, 0.6)", transformOrigin:"50% 400px"})
		.to("#logo", {y:-64, ease:"power2.inOut", delay:2})
		.from("#cta-line", {scaleY:0, ease:"power3.inOut"})
		.from([".cta-logo"], {y:"-=7", stagger:0.5, autoAlpha:0})
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