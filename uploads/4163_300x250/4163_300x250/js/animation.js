var creative = {}; //ad object

function init() {
	console.log("Ad Ready");
	addEventListeners();
	creative.viewport = document.getElementById('mainExit');
    creative.isi_height = document.getElementById('isi-copy').offsetHeight;
	scrollSpeed = creative.isi_height/10;
	gsap.set(['#viewport', '#border', '.gl', '.isi'], {autoAlpha:1});
	// gsap.set(['#tmp'], {alpha:0.5});
	frameOne();
}

function pillDissolve() {
	const x = 1.6
	var tl = gsap.timeline({defaults: {duration: x, ease: "power1.in"}});
    tl
		.set('.pill-dissolve', {x: -4, y: -4, scale: 0.95, rotate: -3})
		
		.set('#gl-pill-dissolve1', {autoAlpha: 1})
        .to('#gl-pill-dissolve1', {duration: x*2, rotate: 0}, '<')
		.to('#gl-pill-dissolve1', {delay: x, autoAlpha: 0}, '<')

		.to('#gl-pill-dissolve2', {autoAlpha: 1}, '<')
		.to('#gl-pill-dissolve2', {duration: x*2, rotate: 0}, '<')
		.to('#gl-pill-dissolve2', {delay: 1.8, autoAlpha: 0}, '<')

		.to('#gl-pill-dissolve3', {autoAlpha: 1}, '<')
		.to('#gl-pill-dissolve3', {duration: x*2, rotate: 0}, '<')
		.to('#gl-pill-dissolve3', {delay: x, autoAlpha: 0}, '<')

		.to('#gl-pill-dissolve4', {autoAlpha: 1}, '<')
		.to('#gl-pill-dissolve4', {duration: x*2, rotate: 0}, '<')
		.to('#gl-pill-dissolve4', {delay: x, autoAlpha: 0}, '<')

		.to('#gl-pill-dissolve5', {autoAlpha: 1}, '<')
		.to('#gl-pill-dissolve5', {duration: x*2, rotate: 0}, '<')
		.to('#gl-pill-dissolve5', {delay: x, autoAlpha: 0}, '<')

		.to('#gl-pill-dissolve6', {autoAlpha: 1}, '<')
		.to('#gl-pill-dissolve6', {duration: x*2 + 0.2, rotate: 0}, '<')
}


function frameOne() {
	pillDissolve();
	gsap.set('.f1', {autoAlpha:1});

	const delay = 4;
	gsap.to('.f1', {delay: delay -0.3, duration: 0.3, autoAlpha: 0})
    gsap.delayedCall(delay, frameTwo);
}

function frameTwo() {
	gsap.to('.f2', {duration: 0.3, autoAlpha:1});

	const delay = 4;
	gsap.to('.f2', {delay: delay -0.3, duration: 0.3, autoAlpha: 0})
    gsap.delayedCall(delay, frameThree);
}

function frameThree() {
	gsap.to('.f3', {duration: 0.3, autoAlpha:1});

	const delay = 4;
	gsap.to('.f3, #gl-pill-dissolve6', {delay: delay -0.3, duration: 0.3, autoAlpha: 0})
    gsap.delayedCall(delay, frameFour);
}

function frameFour() {
	gsap.to('.f4', {duration: 0.3, autoAlpha:1});
	gsap.to('#gl-pill', {duration: 1.2, autoAlpha:1, onComplete: ISIscroll});
}


// ISI Scroll
function ISIscroll() {
	gsap.delayedCall(0, timelineBegin);
    var timer = gsap.timeline();
        isiAnim = gsap.timeline()
        ISI = document.getElementById('isi-copy-con');
    timer.play();

	function timelineBegin(){ isiAnim.to('#isi-copy-con', {duration:1, scrollTo: {y:"+=10"}, ease:"none", repeat:scrollSpeed, repeatRefresh:true, z:0.1, rotationZ:0.01, force3D:true }); }

    ISI.addEventListener('mouseover', mouseInner, false);
    function mouseInner() { ISI.removeEventListener('mouseover', mouseInner, false); timer.pause(); isiAnim.clear(); ISI.addEventListener('mouseout', mouseOuter, false); function mouseOuter() { ISI.addEventListener('mouseover', mouseInner, false); timer.play(); var currentTime = timer.totalTime(); if (currentTime < scrollSpeed-1) { timelineBegin(); } } }
}

function addEventListeners() { 
    function mainExitHandler(e) { Enabler.exit('MainExit'); }
	function PIExitHandler(e) { Enabler.exit('PI Exit'); }
	function medWatchExitHandler(e) { Enabler.exit('Med Watch Exit'); }
    document.getElementById('mainExit').addEventListener('click', mainExitHandler, false);
	document.getElementById('PIExit1').addEventListener('click', PIExitHandler, false);
	document.getElementById('PIExit2').addEventListener('click', PIExitHandler, false);
	document.getElementById('medWatchExit').addEventListener('click', medWatchExitHandler, false);
}