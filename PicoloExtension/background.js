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
                    .then(res => res.json())
                    .then(console.log)
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
