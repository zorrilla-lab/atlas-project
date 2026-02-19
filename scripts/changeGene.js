const dropdown = document.getElementById("gene-of-interest-dropdown");
const field = document.getElementById("gene-of-interest-name");

selectElement.addEventListener('change', (e) => {
  const selectedValue = e.target.value;
  field.textContent = selectedValue;
});