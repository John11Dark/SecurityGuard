const speedBar = document.querySelector("#speedBar");
const video = document.querySelector("#videoStream");
const expandMenu = document.querySelector("#expandMenu");
const sideBar = document.querySelector(".asideControllersMain");
let root = document.documentElement;

const userNameLabel = document.querySelectorAll(".userName");
const batteryPowerInfo = document.querySelector("#batteryPowerInfo");
const batteryStatus = document.querySelector(".securityGuardBatteryInfo");
const carTemperature = document.querySelector("#carTemperature");
const temperatureStatus = document.querySelector(".securityGuardTemperature");
const roomTemperature = document.querySelector("#roomTemperature");
const leftSensorReadingsLabel = document.querySelector("#leftSensorReadings");
const rightSensorReadingsLabel = document.querySelector("#rightSensorReadings");
const wheelDirectory = "wheel";
const servoDirectory = "servo";
const minutes = 0.05555555;
const interval = minutes * 60 * 1000;

// power off button
const powerOffButton = document.querySelector("#powerOffButton");
// wheel direction buttons
const forwardButton = document.querySelector("#forwardButton");
const backwardButton = document.querySelector("#backwardButton");
const leftButton = document.querySelector("#leftButton");
const rightButton = document.querySelector("#rightButton");
// buzzer button

const buzzerButton = document.querySelector("#buzzerButton");

// servo direction buttons
const upServoButton = document.querySelector("#servoUpButton");
const rightServoButton = document.querySelector("#servoRightButton");
const centerServoButton = document.querySelector("#servoCenterButton");
const downServoButton = document.querySelector("#servoDownButton");
const leftServoButton = document.querySelector("#servoLeftButton");

const distanceButton = document.querySelector("#ultraSonicButton");
const distanceLabel = document.querySelector("#ultraSonicLabel");
const lightButton = document.querySelector("#lightSensorButton");
const leftLightSensorLabel = document.querySelector("#leftSensorReadings");
const rightLightSensorLabel = document.querySelector("#rightSensorReadings");

const ultrasonicModeButton = document.querySelector("#ultraSonic");
const lineTrackingModeButton = document.querySelector("#lineTracking");
const lightTrackingModeButton = document.querySelector("#lightTracking");
const faceTrackingModeButton = document.querySelector("#faceTracking");
const voiceCommandsModeButton = document.querySelector("#voiceCommand");

const UltrasonicReadingsLabel = document.querySelector("#ultraSonicLabel");

// LEDs buttons
// animation buttons
const RGBAnimationBtn = document.querySelector("#RGB_Button");
const rainbowAnimationBtn = document.querySelector("#rainbowAnimationBtn");
const cycleAnimationBtn = document.querySelector("#cycleAnimationBtn");
const randomAnimationBtn = document.querySelector("#randomAnimationBtn");
const chaserAnimationBtn = document.querySelector("#chaserAnimation");
// single lED button
const LEDIndexOne = document.querySelector("#btnOne");
const LEDIndexTwo = document.querySelector("#btnTwo");
const LEDIndexThree = document.querySelector("#btnThree");
const LEDIndexFour = document.querySelector("#btnFour");
const LEDIndexFive = document.querySelector("#btnFive");
const LEDIndexSix = document.querySelector("#btnSix");
const LEDIndexSeven = document.querySelector("#btnSeven");
const LEDIndexEight = document.querySelector("#btnEight");
const LEDIndexAll = document.querySelector("#btnOFF");

const colorPicker = document.querySelector("#ColorPicker");

function hexToRgb(HEX) {
  let RGB = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(HEX);
  return RGB
    ? {
        R: parseInt(RGB[1], 16),
        G: parseInt(RGB[2], 16),
        B: parseInt(RGB[3], 16),
      }
    : null;
}

async function getData() {
  fetch(`${window.origin}/data`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      userNameLabel.forEach((label) => {
        label.textContent = data.username;
      });
      carTemperature.textContent = setStatus(
        (type = "Temperature"),
        (statusValue = data.Temperature)
      );
      batteryPowerInfo.textContent = setStatus(
        (type = "Battery"),
        (statusValue = data.power)
      );

      roomTemperature.textContent = setStatus(
        (type = "Temperature"),
        (statusValue = data.roomTemperature)
      );

      UltrasonicReadingsLabel.textContent = setStatus(
        (type = "Temperature"),
        (statusValue = data.dataDistance)
      );

      leftLightSensorLabel.textContent = data.leftSensorReadings;
      rightLightSensorLabel.textContent = data.rightSensorReadings;
    });
}

colorPicker.addEventListener("change", () => {
  root.style.setProperty("--_ColorPicker", colorPicker.value);
});

// side menu buttons
function menuExpanded(isExpanded) {
  expandMenu.setAttribute("isExpanded", isExpanded);
  sideBar.setAttribute("aria-expanded", isExpanded);
}

expandMenu.addEventListener("click", () => {
  let isExpanded = expandMenu.getAttribute("isExpanded");
  if (isExpanded === "false") {
    menuExpanded((isExpanded = true));
  } else if (isExpanded === "true") {
    menuExpanded((isExpanded = false));
  }
});

speedBar.addEventListener("click", () => {
  speedBar.setAttribute("value", speedBar.value);
});

function setStatus(type, statusValue) {
  statusValue = parseInt(statusValue);
  if (type == "Temperature") {
    if (statusValue <= 60 && statusValue >= 45) {
      temperatureStatus.setAttribute("status", "veryHigh");
    } else if (statusValue <= 42) {
      temperatureStatus.setAttribute("status", "high");
    } else if (statusValue <= 35) {
      temperatureStatus.setAttribute("status", "good");
    }
  }
  if (type == "Battery") {
    if (statusValue <= 100 && statusValue >= 26) {
      batteryStatus.setAttribute("status", "good");
    } else if (statusValue <= 25) {
      batteryStatus.setAttribute("status", "low");
    } else if (statusValue <= 15) {
      batteryStatus.setAttribute("status", "veryLow");
    }
  }
  return statusValue;
}

async function onLoad() {
  colorPicker.value = "#ffffff";
  root.style.setProperty("--_ColorPicker", colorPicker.value);
}

// Video
/* async function videoStream() {
  fetch(`${window.origin}/${"video_feed"}`);
  video.srcObject = `${window.origin}/${"video_feed"}`;
}

videoStream(); */

function sendClickRequestWheel(object, directory, objectAttribute) {
  object.addEventListener("mousedown", () => {
    fetch(`${window.origin}/${directory}/${objectAttribute}`);
    console.log("sending request ");
  });
  object.addEventListener("mouseup", () => {
    fetch(`${window.origin}/${directory}/stop}`);
    console.log("request sent");
  });
}

function sendClickRequestServo(object, direction, oppositeObject = null) {
  object.addEventListener("click", () => {
    let directionValue = parseInt(object.getAttribute("directionValue"));
    if (direction == "Center") {
      upServoButton.setAttribute("directionValue", directionValue);
      rightServoButton.setAttribute("directionValue", directionValue);
      downServoButton.setAttribute("directionValue", directionValue);
      leftServoButton.setAttribute("directionValue", directionValue);
    } else if (direction == "down" || direction == "left") {
      if (directionValue < 180 && directionValue >= 0) {
        directionValue += 10;
        console.log(directionValue);
        object.setAttribute("directionValue", directionValue);
        oppositeObject.setAttribute("directionValue", directionValue);
      }
    } else if (direction == "up" || direction == "right") {
      if (directionValue <= 180 && directionValue > 0) {
        directionValue -= 10;
        object.setAttribute("directionValue", directionValue);
        oppositeObject.setAttribute("directionValue", directionValue);
      }
    }
    fetch(`${window.origin}/servo/${direction}`, {
      method: "POST",
      credentials: "include",
      body: directionValue,
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json",
      }),
    });
  });
}

function LedButton(object, directory, objectStatus) {
  object.addEventListener("click", () => {
    if (object.getAttribute("ledStatus") === "off") {
      object.setAttribute("ledStatus", "on");
      fetch(
        `${window.origin}/LEDs/${directory}/${object.getAttribute("ledStatus")}`
      );
      console.log(
        `request sent with state ${object.getAttribute("ledStatus")}`
      );
    } else if (object.getAttribute("ledStatus") === "on") {
      object.setAttribute("ledStatus", "off");
      fetch(`${window.origin}/LEDs/${directory}/off`);
      console.log(
        `request sent with state ${object.getAttribute("ledStatus")}`
      );
    }
  });
}

function singleLedRequest(object, index) {
  if (index != 0) {
    object.addEventListener("click", () => {
      let hexValue = colorPicker.value;
      let ledStatus = object.getAttribute("ledStatus");
      if (ledStatus === "off") {
        object.setAttribute("ledStatus", "on");
      } else if (ledStatus === "on") {
        object.setAttribute("ledStatus", "off");
      }
      data = {
        index: index,
        RGB: hexToRgb(hexValue),
        State: object.getAttribute("ledStatus"),
      };
      fetch(
        `${window.origin}/LEDs/single/${object.getAttribute("ledStatus")}`,
        {
          method: "POST",
          credentials: "include",
          body: JSON.stringify(data),
          cache: "no-cache",
          headers: new Headers({
            "content-type": "application/json",
          }),
        }
      );
    });
  }
}

function setCarMode(object, directory) {
  lightTrackingModeButton.setAttribute("modeStatus", "close");
  lineTrackingModeButton.setAttribute("modeStatus", "close");
  ultrasonicModeButton.setAttribute("modeStatus", "close");
  faceTrackingModeButton.setAttribute("modeStatus", "close");

  object.addEventListener("click", () => {
    let objectMode = object.getAttribute("modeStatus");
    if (objectMode === "start") {
      fetch(`${window.origin}/sensor/${directory}/${objectMode}`);
      object.setAttribute("modeStatus", "close");
      console.log(`request sent with status ${objectMode} to start`);
    } else if (objectMode === "close") {
      fetch(`${window.origin}/sensor/${directory}/${objectMode}`);
      object.setAttribute("modeStatus", "start");
      console.log(`request sent with status ${objectMode} to close`);
    }
  });
}

onLoad();

// wheels request
sendClickRequestWheel(
  (object = forwardButton),
  (directory = wheelDirectory),
  (objectAttribute = object.getAttribute("Direction"))
);
sendClickRequestWheel(
  (object = backwardButton),
  (directory = wheelDirectory),
  (objectAttribute = object.getAttribute("Direction"))
);
sendClickRequestWheel(
  (object = rightButton),
  (directory = wheelDirectory),
  (objectAttribute = object.getAttribute("Direction"))
);
sendClickRequestWheel(
  (object = leftButton),
  (directory = wheelDirectory),
  (objectAttribute = object.getAttribute("Direction"))
);
sendClickRequestWheel(
  (object = buzzerButton),
  (directory = wheelDirectory),
  (objectAttribute = object.getAttribute("Direction"))
);
// servo request

sendClickRequestServo(
  (object = upServoButton),
  (objectAttribute = object.getAttribute("direction")),
  (oppositeObject = downServoButton)
);
sendClickRequestServo(
  (object = downServoButton),
  (objectAttribute = object.getAttribute("direction")),
  (oppositeObject = upServoButton)
);
sendClickRequestServo(
  (object = centerServoButton),
  (objectAttribute = object.getAttribute("direction"))
);
sendClickRequestServo(
  (object = leftServoButton),
  (objectAttribute = object.getAttribute("direction")),
  (oppositeObject = rightServoButton)
);
sendClickRequestServo(
  (object = rightServoButton),
  (objectAttribute = object.getAttribute("direction")),
  (oppositeObject = leftServoButton)
);

LedButton(
  (object = RGBAnimationBtn),
  (directory = object.getAttribute("directory")),
  (objectStatus = object.getAttribute("ledStatus"))
);

LedButton(
  (object = cycleAnimationBtn),
  (directory = object.getAttribute("directory")),
  (objectStatus = object.getAttribute("ledStatus"))
);

LedButton(
  (object = randomAnimationBtn),
  (directory = object.getAttribute("directory")),
  (objectStatus = object.getAttribute("ledStatus"))
);

LedButton(
  (object = chaserAnimationBtn),
  (directory = object.getAttribute("directory")),
  (objectStatus = object.getAttribute("ledStatus"))
);

LedButton(
  (object = rainbowAnimationBtn),
  (directory = object.getAttribute("directory")),
  (objectStatus = object.getAttribute("status"))
);

singleLedRequest(
  (object = LEDIndexOne),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexTwo),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexThree),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexFour),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexFive),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexSix),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexSeven),
  (index = object.getAttribute("index"))
);
singleLedRequest(
  (object = LEDIndexEight),
  (index = object.getAttribute("index"))
);

singleLedRequest(
  (object = LEDIndexAll),
  (index = object.getAttribute("index"))
);

setCarMode(
  (object = ultrasonicModeButton),
  (directory = object.getAttribute("directory"))
);
setCarMode(
  (object = lineTrackingModeButton),
  (directory = object.getAttribute("directory"))
);
setCarMode(
  (object = lightTrackingModeButton),
  (directory = object.getAttribute("directory"))
);

setInterval(() => {
  getData();
}, interval);

powerOffButton.addEventListener("click", () => {
  let disconnect = confirm("are you sure you want to exit? 😟");
  if (disconnect) {
    alert("good bye!👋\nsmart car will be down in few seconds😟");
    fetch(`${window.origin}/server/disconnect`);
  } else {
    alert("Ok i wont! 😊");
  }
});
