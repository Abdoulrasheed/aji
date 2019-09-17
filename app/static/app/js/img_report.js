var dwn = document.querySelector('#download_img');
html2canvas(document.querySelector("#capture")).then(canvas => {
	var context = canvas.getContext("2d");
	var img = new Image();
	img.onload = ()=> {
		context.drawImage(img, 0, 0);
	};

	var strDataURI = canvas.toDataURL();
	img.src = strDataURI;
	dwn.setAttribute('href', img.src);
});

dwn.addEventListener('click', ()=>{
	dwn.setAttribute('download', 'Report.png');
});