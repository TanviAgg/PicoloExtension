var screenshot = {
  content: document.createElement("canvas"),
  data: "",

  init: function () {
    this.initEvents();
  },

  saveScreenshot: function (dimensions) {
    var image = new Image();
    image.onload = function () {
      var canvas = screenshot.content;
      canvas.width = dimensions.width;
      canvas.height = dimensions.height;
      var context = canvas.getContext("2d");
      context.drawImage(
        image,
        dimensions.left,
        dimensions.top,
        dimensions.width,
        dimensions.height,
        0,
        0,
        dimensions.width,
        dimensions.height
      );

      // send the image to server for processing
      fetch('http://localhost:5000', {
                      method: 'POST',
                      body: JSON.stringify({
                        title: 'image to load',
                        body: screenshot.content.toDataURL()
                      }),
                      headers: {
                        'Content-type': 'application/json; charset=UTF-8'
                      }
                    })
                    .then(res => {
                      res.json()
                          .then(val =>
                              copyTextToClipboard(val)
                          );
                    }
                    )
      screenshot.data = "";
    };
    image.src = screenshot.data;
  },

  initEvents: function () {
    chrome.commands.onCommand.addListener(function (command) {
      console.log("Command:", command);
      captureScreen();
    });
    chrome.browserAction.onClicked.addListener(function (tab) {
      captureScreen();
    });
  },
};

let captureScreen = () => {
  chrome.browserAction.setBadgeText({ text: "picolo" });
  console.log("uo");
  chrome.tabs.captureVisibleTab(
    null,
    {
      format: "png",
      quality: 100,
    },
    function (data) {
      screenshot.data = data;

      // send an alert message to webpage
      chrome.tabs.query(
        {
          active: true,
          currentWindow: true,
        },
        function (tabs) {
          chrome.tabs.sendMessage(tabs[0].id, { ready: "ready" }, function (
            response
          ) {
            if (response.download === "download") {
              screenshot.saveScreenshot(response.content);
            } else {
              screenshot.data = "";
            }
          });
        }
      );
    }
  );
};

screenshot.init();

function copyTextToClipboard(text) {
  //Create a textbox field where we can insert text to.
  var copyFrom = document.createElement("textarea");

  //Set the text content to be the text you wished to copy.
  copyFrom.textContent = text;

  //Append the textbox field into the body as a child.
  //"execCommand()" only works when there exists selected text, and the text is inside
  //document.body (meaning the text is part of a valid rendered HTML element).
  document.body.appendChild(copyFrom);

  //Select all the text!
  copyFrom.select();
  document.execCommand('copy');
  //(Optional) De-select the text using blur().
  copyFrom.blur();

  //Remove the textbox field from the document.body, so no other JavaScript nor
  //other elements can get access to this.
  document.body.removeChild(copyFrom);
}