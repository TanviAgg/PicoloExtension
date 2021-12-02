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

      // save the image
      var link = document.createElement("a");
      link.download = "download.png";
      link.href = screenshot.content.toDataURL();
      doOCR(screenshot.content.toDataURL());
      link.click();
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

const doOCR = async (image) => {
  //const image = document.getElementById("image");
  //const result = document.getElementById("result");

  const { createWorker } = Tesseract;
  const worker = createWorker({
    workerPath: chrome.runtime.getURL("js/worker.min.js"),
    langPath: chrome.runtime.getURL("traineddata"),
    corePath: chrome.runtime.getURL("js/tesseract-core.wasm.js"),
  });

  await worker.load();
  await worker.loadLanguage("eng");
  await worker.initialize("eng");
  const {
    data: { text },
  } = await worker.recognize(image);
  console.log(text);
  // result.innerHTML = `<p>OCR Result:</p><p>${text}</p>`;
  await worker.terminate();
};

screenshot.init();
