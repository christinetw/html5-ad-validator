var main, clickable;
var endFrameOffer;
var vehicle;
var logo;
var ctaTxt;
var background;
var defaultAd;


function init() {

    console.log("INIT")

    main = document.querySelector("#viewport");
    clickable = document.querySelector("#clickable");

    canvas = document.getElementById("canvas");
    anim_container = document.getElementById("animation_container");
    dom_overlay_container = document.getElementById("dom_overlay_container");

    dynamicFeedInitialization();

    eventListeners();

}



var offerTxt, vehicleImageSrc, logoSrc, fontSizeSrc, fontLineHeightSrc, ctaTxtSrc, exitURL, txt_colour;

function dynamicFeedInitialization() {

    // Dynamic Content variables and sample values
    Enabler.setProfileId(10517133);
    var devDynamicContent = {};
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250 = [{}];
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0]._id = 0;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Offer_ID = 1970;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Unique_ID = 1;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Reporting_Label = "Alberta_WeeklyFinancing_Pacifica";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].offerType = "Weekly Financing";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].vehicle_image_URL = {};
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].vehicle_image_URL.Url = "https://www.chrysler.ca/imagesAS/iof.php?width=600&year=2020&image=CC20_RUCR53_2DW_PRV_APA_XXX_XXX_XXX.png";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].logo_image_URL = {};
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].logo_image_URL.Type = "file";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].logo_image_URL.Url = "https://s0.2mdn.net/creatives/assets/4501114/DAA_Chrysler_300x250_LogoWhite_spacing_correction.png";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].offer_text = "<strong>2021 chrysler Pacifica<br><\/strong><strong>$107<\/strong> WEEKLY FINANCING<sup>\u2020<\/sup><br>@ <strong>3.99%<\/strong> FOR <strong>96<\/strong> MONTHS<br><sup>WITH $0 DOWN<\/sup>";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].text_size = 18;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].text_lineHeight = 20;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].txt_colour = "#000";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].CTA_txt = "EXPLORE DEALS";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Exit_URL = {};
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Exit_URL.Url = "https://www.chrysleroffers.ca/en/offers/pacifica?source=ad&utm_medium=Display&utm_source=Dynamic&utm_campaign=chryslerpacifica_WeeklyFinancing_chrysler_pacifica_alberta_$107_@3.99percent_96months_$0down_300x250_Standard_2020_1970&utm_content=EN_REG__HD_na";
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Default = false;
    devDynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Active = true;
    Enabler.setDevDynamicContent(devDynamicContent);

    vehicleImageSrc = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].vehicle_image_URL.Url;
    logoSrc = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].logo_image_URL.Url;
    offerTxt = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].offer_text;
    fontSizeSrc = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].text_size;
    fontLineHeightSrc = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].text_lineHeight;
    txt_colour = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].txt_colour;
    ctaTxtSrc = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].CTA_txt;
    exitURL = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Exit_URL.Url;
    defaultAd = dynamicContent.DAA2020_CHRYSLER_PACIFICA_Feb_EN_300x250[0].Default;

    console.log("Vehicle Image:", vehicleImageSrc, "Exit URL:", exitURL)

    vehicle = document.querySelector("#vehicle");
    logo = document.querySelector("#logo");
    endFrameOffer = document.querySelector("#endFrameOffer");
    ctaTxt = document.querySelector("#ctaTxt");

    vehicle.style.backgroundImage = "url(" + vehicleImageSrc + ")";
    logo.style.backgroundImage = "url(" + logoSrc + ")";
    endFrameOffer.innerHTML = offerTxt;
    endFrameOffer.style.fontSize = '' + fontSizeSrc + 'px';
    endFrameOffer.style.lineHeight = '' + fontLineHeightSrc + 'px';
    endFrameOffer.style.color = txt_colour;
    endFrameOffer.style.textTransform = "uppercase"
    ctaTxt.innerHTML = ctaTxtSrc;

    checkDefault();


}

function elem(id) {
    return document.querySelector(id)
}

function checkDefault(){
console.log('checkdefault')
    if (defaultAd === true) {
        showBackup()
    } else { 
        setDynamic() };
}

function showBackup(){
    console.log(clickable)
    elem('#clickable').style.background = "url('images/backup.jpg') no-repeat";

    TweenMax.set(clickable, { autoAlpha: 1 })
    
    console.log("default")
}

function setDynamic() {

    TweenMax.set(border, { alpha: 1 })

    TweenMax.set(background1_1, { alpha: 1 })
    TweenMax.set(logo, { alpha: 1 })


    frameOne();
}

function eventListeners() {

    console.log("Setting Buttons");

    clickable.style.cursor = "pointer"
    clickable.addEventListener("click", mainExit, false);

    //clickable.addEventListener("mouseover", bannerOver, false);
    //clickable.addEventListener("mouseout", bannerOut, false);
}


function frameOne() {
    var d = 4;
    TweenMax.fromTo(text1_1, 0.5, { alpha: 0, x: -250 }, { alpha: 1, x: 0 })

    TweenMax.delayedCall(d, frameTwo);
}

function frameTwo() {
    var d = 3;

    TweenMax.to(text1_1, 0.5, { alpha: 0, x: -250 })

    TweenMax.fromTo(text2_1, 0.5, { alpha: 0, x: 250 }, { alpha: 1, x: 0 })

    TweenMax.to(text2_1, 0.5, { delay:3, alpha: 0, x: -250 })


    
    //**comment in and out for skipping frames 3-4
    TweenMax.delayedCall(d, frameThree); //frame 3 in//
    // TweenMax.set([background2_1], { alpha: 1 }) //frame 3 out//
    // TweenMax.from([background2_1], 0.5, { x: 300, delay:d }) //frame 3 out//
    // TweenMax.delayedCall(d, frameFour); //frame 3 out//
}

function frameThree() {
    var d = 4;
    TweenMax.set([background2_1, eventLogo, vehicle], { alpha: 1 })
    TweenMax.from(logoText, 0.6, { delay: 2.25, alpha: 0, x: "+=15" })
    
    TweenMax.from([background2_1], 0.5, { x: 300 })
    
    TweenMax.from(vehicle, 0.75, {delay:0.5, alpha:0})
    TweenMax.from([eventLogo], 0.5, {delay:0.5, alpha:0, scale:0,force3D:false, rotation:0.01, skewX:0.01, perspective:1000, z:0.01})

    TweenMax.delayedCall(d, frameFour);

}

function frameFour() {
    console.log("END FRAME")

    // TweenMax.to([ logoText, background], 0.4, { alpha: 0 })

    TweenMax.set([cta, ctaTxt, ctaBall], { alpha: 1 })

    TweenMax.from([cta, ctaBall], 0.7, { delay: 2, alpha: 0, onComplete: addEventListeners })

    TweenMax.set([endFrameOffer], { alpha: 1 })

    //**comment in and out for skipping frames 3-4
    TweenMax.to(eventLogo, 0.5, {alpha:0}) //frame 3 in//
    // TweenMax.set(vehicle, { alpha: 1 }) //frame 3 out//
    // TweenMax.from(vehicle, 0.5, { delay: 0.5, alpha: 0 })//frame 3 out//

    TweenMax.from(endFrameOffer, 0.4, { delay: 0.2, alpha: 0 })
}

function addEventListeners() {
    clickable.addEventListener('mouseover', mouseover)
    clickable.addEventListener('mouseout', mouseout)
    mouseover()
    TweenMax.delayedCall(0.2, mouseout)
}

function mouseover() {
    TweenMax.to(ctaBall, 0.15,{ x:"3px",force3D:false, rotation:0.01, skewX:0.01, perspective:1000, z:0.01})
}

function mouseout() {
    TweenMax.to(ctaBall, 0.15,{ x:"0px", force3D:false, rotation:0.01, skewX:0.01, perspective:1000, z:0.01})
}

function mainExit(e){
	console.log("CLICKING")
	Enabler.exitOverride("Main Exit", exitURL);
}