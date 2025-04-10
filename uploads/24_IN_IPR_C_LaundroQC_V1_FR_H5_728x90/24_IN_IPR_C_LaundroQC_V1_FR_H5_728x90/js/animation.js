var creative = {}; //ad object

function init() {
	console.log("Ad Ready");
	creative.viewport = document.getElementById("viewport");
	gsap.set(["#viewport", "#border"], {autoAlpha:1});

	// gsap.set(['#tmp'], {alpha:0.4});

	frameOne();
}

function frameOne() {
	gsap.set(['.f1', '.gl'], {autoAlpha: 1});

	gsap.from(['#gl-bg'], {duration: 19, scale:1.1, ease:'linear.easeNone'});

	var tl = gsap.timeline({delay: 0.2});
	tl
		.from(['.f1-copy'], {duration: 1.2, autoAlpha: 0, y:10, stagger:0.18, ease:'elastic.out(0.1,5)'})

	var frameDelay = 4;
	gsap.to(['.f1-copy'], {duration: 1, autoAlpha: 0, y:-10, ease:'elastic.inOut(0.1,5)', delay:frameDelay});
	gsap.delayedCall(frameDelay+0.8, frameTwo);
}

function frameTwo() {
	gsap.set(['.f2'], {autoAlpha: 1});
	
	gsap.from(['.f2-copy'], {delay: 0.2, duration: 1.2, autoAlpha: 0, y:10, stagger:0.18, ease:'elastic.out(0.1,5)'});
	
	var frameDelay = 4;
	gsap.to(['.f2-copy'], {duration: 1, autoAlpha: 0, y:-10, transformOrigin: "bottom center", ease:'elastic.inOut(0.1,5)', delay:frameDelay});
	gsap.delayedCall(frameDelay+0.8, endFrame);
}

function endFrame() {
	gsap.set(['.ef'], {autoAlpha: 1});
	
	gsap.to(['#f1-hero'], {delay: 0.4, duration: 0.5, autoAlpha: 0});
	gsap.from(['#ef-hero'], {delay: 0.4, duration: 0.5, autoAlpha: 0});

	var tl = gsap.timeline({delay:0.4});
	tl
	.from(['.ef-copy'], {duration: 0.4, autoAlpha: 0, y:10, stagger:0.18})
	.from(["#ef-cta"], {delay: 0.5, autoAlpha: 0, duration: 0.3})
}