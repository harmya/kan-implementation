// Graph container and state variables
const graph = document.getElementById("graph");
let currentColor = "red";

// Initialize the first button as active
document.querySelector(".button.red").classList.add("active");

// Array to track points
const points = [];

const fetchPlot = async () => {
  console.log("Submitting points:", points);
  const response = await fetch("/plot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(points),
  });

  const plot = await response.json();
  console.log(plot);
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

  // Log the point and the array
  console.log(`Point added: X=${x}, Y=${y}, Color=${currentColor}`);
  console.log("All points:", points);
});

document.querySelectorAll("button").forEach((button) => {
  if (button.id === "submit") {
    return;
  }
  button.addEventListener("click", (event) => {
    // Update current color
    currentColor = event.target.classList[1];
    console.log(`Current color: ${currentColor}`);

    // Update active button styling
    document.querySelectorAll("button").forEach((btn) => {
      btn.classList.remove("active");
    });
    event.target.classList.add("active");
  });
});

document.getElementById("submit").addEventListener("click", fetchPlot);
