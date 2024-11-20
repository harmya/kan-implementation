// Graph container and state variables
const graph = document.getElementById("graph");
let currentColor = "red";
let k = 3;

const mapping = {
  3: "three",
  5: "five",
  7: "seven",
};

// Initialize the first button as active
document.querySelector(".button.red").classList.add("active");
document.querySelector(".button.three").classList.add("active");

// Array to track points
const points = [];

const fetchPlot = async () => {
  const data = {
    points,
    k,
  };

  const response = await fetch("/plot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const plot = await response.json();
  // Get the div with id "output"
  const outputDiv = document.getElementById("output");

  // Set the innerHTML to an <img> tag with the base64 string as src
  if (plot.img_data) {
    outputDiv.innerHTML = `<img src="data:image/png;base64,${plot.img_data}" alt="Generated Plot" />`;
  } else {
    outputDiv.innerHTML = "Failed to generate plot.";
  }
};

// Add event listener to the graph for point creation
graph.addEventListener("click", (event) => {
  // Get position relative to the graph container
  const rect = graph.getBoundingClientRect();
  const x = event.clientX - rect.left;
  let y = event.clientY - rect.top;

  if (x < 5 || x > rect.width - 5 || y < 5 || y > rect.height - 5) {
    return;
  }

  // Create a new point element
  const point = document.createElement("div");
  point.className = "point";
  point.style.left = `${x}px`;
  point.style.top = `${y}px`;
  point.style.backgroundColor = currentColor;

  // Add the point to the graph
  graph.appendChild(point);

  y = rect.height - y;
  points.push({ x, y, color: currentColor });
});

document.querySelectorAll("button").forEach((button) => {
  if (button.id === "submit") {
    return;
  }

  if (button.id === "clear") {
    button.addEventListener("click", () => {
      // Clear the graph
      const outputDiv = document.getElementById("output");
      outputDiv.innerHTML = "";
      graph.innerHTML = "";
      points.length = 0;
    });
    return;
  }

  button.addEventListener("click", (event) => {
    if (button.id === "value") {
      k = parseInt(document.getElementById("k").value);
      document.querySelectorAll("button").forEach((btn) => {
        if (btn.classList[1] !== mapping[k] && btn.id === "value") {
          btn.classList.remove("active");
        }
      });
      event.target.classList.add("active");
      return;
    }

    // Update current color
    currentColor = event.target.classList[1];

    // Update active button styling
    document.querySelectorAll("button").forEach((btn) => {
      if (btn.id !== "value" && btn.id !== "clear") {
        btn.classList.remove("active");
      }
    });
    event.target.classList.add("active");
  });
});

document.getElementById("submit").addEventListener("click", fetchPlot);
