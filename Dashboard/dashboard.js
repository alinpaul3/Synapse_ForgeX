// 🔹 INSTALL BUTTON
function installExtension() {
  alert("Go to chrome://extensions → Enable Developer Mode → Load Unpacked → Select extension folder");
}

// 🔹 GET USER ID
const params = new URLSearchParams(window.location.search);
const user_id = params.get("user_id");

// 🔹 ELEMENTS
const installSection = document.getElementById("installSection");
const loadingSection = document.getElementById("loadingSection");
const resultSection = document.getElementById("resultSection");

// 🔹 IF NO USER → SHOW INSTALL
if (!user_id) {
  installSection.classList.remove("hidden");
} else {
  installSection.classList.add("hidden");
  loadingSection.classList.remove("hidden");

  // 🔥 POLLING
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/processed-data/${user_id}`);
      const data = await res.json();

      // ✅ IF RESULT READY
      if (data.ml_output) {
        clearInterval(interval);

        loadingSection.classList.add("hidden");
        resultSection.classList.remove("hidden");

        const result = data.ml_output;

        // USER INFO
        document.getElementById("user").innerText = "User: " + user_id;
        document.getElementById("confidence").innerText =
          "Confidence: " + (result.confidence * 100).toFixed(1) + "%";

        document.getElementById("explanation").innerText =
          result.explanation;

        // CHART
        new Chart(document.getElementById('chart'), {
          type: 'bar',
          data: {
            labels: ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"],
            datasets: [{
              label: "OCEAN Scores",
              data: [
                result.ocean.openness,
                result.ocean.conscientiousness,
                result.ocean.extraversion,
                result.ocean.agreeableness,
                result.ocean.neuroticism
              ]
            }]
          }
        });
      }

    } catch (err) {
      console.error(err);
    }
  }, 3000);
}



// const params = new URLSearchParams(window.location.search);
// const user_id = params.get("user_id");

// console.log("USER ID:", user_id);

// if (!user_id) {
//   console.error("❌ No user_id in URL");
// } else {
//   loadData();
// }

// async function loadData() {
//   try {
//     console.log("Fetching data...");

//     const res = await fetch(`http://127.0.0.1:8000/processed-data/${user_id}`);
//     console.log("Response status:", res.status);

//     const data = await res.json();
//     console.log("DATA RECEIVED:", JSON.stringify(data));

//     if (!data || !data.ml_output) {
//       console.log("❌ No ML output found");
//       return;
//     }

//     console.log("✅ ML OUTPUT FOUND:", data.ml_output);

//     const result = data.ml_output;
//     const ocean = result.ocean;

//     // 🔥 Hide get started, show result
//     document.getElementById("get-started").style.display = "none";
//     document.getElementById("result-section").style.display = "block";

//     // 🔥 Fill in user info
//     document.getElementById("user").innerText = "👤 User: " + user_id;
//     document.getElementById("confidence").innerText =
//       "Confidence: " + (result.confidence * 100).toFixed(1) + "%";
//     document.getElementById("explanation").innerText =
//       "💬 " + result.explanation;

//     // 🔥 Render OCEAN chart
//     new Chart(document.getElementById("chart"), {
//       type: "bar",
//       data: {
//         labels: [
//           "Openness",
//           "Conscientiousness",
//           "Extraversion",
//           "Agreeableness",
//           "Neuroticism"
//         ],
//         datasets: [{
//           label: "OCEAN Personality Scores",
//           data: [
//             ocean.openness,
//             ocean.conscientiousness,
//             ocean.extraversion,
//             ocean.agreeableness,
//             ocean.neuroticism
//           ],
//           backgroundColor: [
//             "rgba(255, 99, 132, 0.7)",
//             "rgba(54, 162, 235, 0.7)",
//             "rgba(255, 206, 86, 0.7)",
//             "rgba(75, 192, 192, 0.7)",
//             "rgba(153, 102, 255, 0.7)"
//           ],
//           borderColor: [
//             "rgba(255, 99, 132, 1)",
//             "rgba(54, 162, 235, 1)",
//             "rgba(255, 206, 86, 1)",
//             "rgba(75, 192, 192, 1)",
//             "rgba(153, 102, 255, 1)"
//           ],
//           borderWidth: 2,
//           borderRadius: 6
//         }]
//       },
//       options: {
//         scales: {
//           y: {
//             beginAtZero: true,
//             max: 1,
//             ticks: {
//               color: "#333"
//             }
//           },
//           x: {
//             ticks: {
//               color: "#333"
//             }
//           }
//         },
//         plugins: {
//           legend: {
//             labels: {
//               color: "#333"
//             }
//           }
//         }
//       }
//     });

//   } catch (err) {
//     console.error("FETCH ERROR:", err);
//   }
// }