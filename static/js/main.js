const data_dropdown = document.getElementById("dataset-dropdown");
const goi_dropdown = document.getElementById("gene-of-interest-dropdown");
const visualization = document.getElementById("visualization");
console.log(data_dropdown, goi_dropdown);

// TODO: make sure dataset and goi are valid before running updateVisualization

async function updateVisualization(dataset_value, goi_value) {
  visualization.innerHTML = "<span>loading visualization...</span>";
  try {
    const res = await fetch("/update_visualization", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataset: dataset_value, gene: goi_value }),
    });
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    visualization.innerHTML = `
      <img src="data:image/png;base64,${data.coexp}" />
      <img src="data:image/png;base64,${data.class}" />
      <img src="data:image/png;base64,${data.subclass}" />
      <img src="data:image/png;base64,${data.supertype}" />
    `;
  } catch (err) {
    visualization.innerHTML = `<span>Error: ${err.message}</span>`;
    console.error(err);
  }
}

goi_dropdown.addEventListener("change", (e) => {
  if (data_dropdown.value) {
    updateVisualization(data_dropdown.value, e.target.value);
  }
});
data_dropdown.addEventListener("change", (e) => {
  if (goi_dropdown.value) {
    updateVisualization(e.target.value, goi_dropdown.value);
  }
});
