// Graph container and state variables
const graph = document.getElementById("graph");
let currentColor = "red";
let k = 3;

// Mapping for button labels
const mapping = {
  3: "three",
  5: "five",
  7: "seven",
};

// Initialize active buttons
document.querySelector(".button.red").classList.add("active");
document.querySelector(`.button.${mapping[k]}`).classList.add("active");

// Array to track points
const points = [];

// Function to fetch and display the plot
const fetchPlot = async () => {
  const outputDiv = document.getElementById("output");

  outputDiv.innerHTML = `<div class="loader"></div>`;

  try {
    const response = await fetch("/plot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ points, k }),
    });

    const plot = await response.json();

    if (plot.img_data) {
      outputDiv.innerHTML = `<img src="data:image/png;base64,${plot.img_data}" alt="Generated Plot" style="max-width: 100%; height: auto;" />`;
    } else {
      outputDiv.innerHTML = "Failed to generate plot.";
    }
  } catch (error) {
    outputDiv.innerHTML = "An error occurred while fetching the plot.";
    console.error("Error fetching plot:", error);
  }
};

// Event listener for adding points on the graph
graph.addEventListener("click", (event) => {
  const rect = graph.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  if (x < 5 || x > rect.width - 5 || y < 5 || y > rect.height - 5) return;

  // Add a new point to the graph
  const point = document.createElement("div");
  point.className = "point";
  point.style.left = `${x}px`;
  point.style.top = `${y}px`;
  point.style.backgroundColor = currentColor;
  graph.appendChild(point);

  points.push({ x, y: rect.height - y, color: currentColor });
});

// Event listener for all buttons
document.querySelectorAll("button").forEach((button) => {
  switch (button.id) {
    case "submit":
      button.addEventListener("click", fetchPlot);
      break;

    case "clear":
      button.addEventListener("click", () => {
        document.getElementById("output").innerHTML = "";
        graph.innerHTML = "";
        points.length = 0;
      });
      break;

    default:
      button.addEventListener("click", (event) => {
        if (button.id === "value") {
          k = event.target.textContent;

          document.querySelectorAll("button").forEach((btn) => {
            if (btn.id === "value")
              btn.classList.toggle("active", mapping[k] === btn.classList[1]);
          });
        } else {
          // Update the current color and active button styling
          currentColor = event.target.classList[1];

          document.querySelectorAll("button").forEach((btn) => {
            if (!["value", "clear"].includes(btn.id))
              btn.classList.remove("active");
          });
          event.target.classList.add("active");
        }
      });
  }
});
