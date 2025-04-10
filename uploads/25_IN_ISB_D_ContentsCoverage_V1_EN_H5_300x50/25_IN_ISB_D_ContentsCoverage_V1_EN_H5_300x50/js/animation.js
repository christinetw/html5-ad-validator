var creative = {}; //ad object

function init() {
	console.log("Ad Ready");
	creative.viewport = document.getElementById("viewport");

	gsap.set(["#viewport", "#border"], {autoAlpha:1});

	// gsap.set(["#tmp"], {alpha:0.4});

	frameOne();
}

function frameOne() {
	gsap.set(['.f1', '.gl'], {autoAlpha: 1});

	gsap.from(['.f1-txt'], {duration: 0.5, autoAlpha: 0, y:5});

	var frameDelay = 5.25;
	gsap.to(['.f1'], {duration: 0.3, autoAlpha: 0, delay:frameDelay});
	gsap.delayedCall(frameDelay+0.3, frameTwo);
}

function frameTwo() {
	gsap.set(['.f2'], {autoAlpha: 1});

	gsap.from(['.f2-txt'], {duration: 0.5, autoAlpha: 0, y:5});

	var frameDelay = 2.5;
	gsap.to(['.f2'], {duration: 0.3, autoAlpha: 0, delay:frameDelay});
	gsap.delayedCall(frameDelay+0.3, frameThree);
}

function frameThree() {
	gsap.set(['.f3'], {autoAlpha: 1});


	gsap.from(['.f3-txt'], {duration: 0.5, autoAlpha: 0, y:5});

	var frameDelay = 4;
	gsap.to(['.f3'], {duration: 0.3, autoAlpha: 0, delay:frameDelay});
	gsap.delayedCall(frameDelay+0.3, endFrame);
}

function endFrame() {
	gsap.set(['.ef'], {autoAlpha: 1});

	var tl = gsap.timeline({});
	tl
	.from(['.ef-txt'], {duration: 0.5, autoAlpha: 0, y:10, stagger:0.4})
	.fromTo(["#ef-cta"], {autoAlpha: 0}, {delay: 0.5, duration: 0.3, autoAlpha: 1})
}

