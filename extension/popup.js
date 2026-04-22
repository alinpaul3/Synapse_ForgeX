// document.addEventListener('DOMContentLoaded', () => {

//     const loginButton = document.getElementById('login');
//     const loginStatus = document.getElementById('loginStatus');
//     const platforms = document.querySelectorAll('.platform');
//     const consentCheckbox = document.getElementById('consent');
//     const startButton = document.getElementById('start');
//     const feedback = document.getElementById('platformSelectionFeedback');

//     let selectedPlatforms = [];

//     // 🔐 LOGIN
//     loginButton.addEventListener('click', () => {
//         const email = document.getElementById('email').value;

//         if (!email) {
//             loginStatus.textContent = "Enter email";
//             loginStatus.style.color = "red";
//             return;
//         }

//         localStorage.setItem("user_email", email);

//         loginStatus.textContent = "✅ Logged in as " + email;
//         loginStatus.style.color = "lightgreen";
//     });

//     // 🔥 PLATFORM SELECTION
//     platforms.forEach(platform => {
//         platform.addEventListener('click', () => {
//             const value = platform.dataset.value;

//             if (platform.classList.contains('active')) {
//                 platform.classList.remove('active');
//                 selectedPlatforms = selectedPlatforms.filter(p => p !== value);
//             } else {
//                 if (selectedPlatforms.length >= 2) {
//                     feedback.textContent = "Select only 2 platforms";
//                     return;
//                 }
//                 platform.classList.add('active');
//                 selectedPlatforms.push(value);
//             }

//             updateUI();
//         });
//     });

//     function updateUI() {
//         if (selectedPlatforms.length === 1) {
//             feedback.textContent = "Select one more platform";
//         } else if (selectedPlatforms.length === 2) {
//             feedback.textContent = "Ready ✅";
//         } else {
//             feedback.textContent = "Select 2 platforms";
//         }

//         updateStartButton();
//     }

//     // 🔥 ENABLE BUTTON
//     function updateStartButton() {
//         const email = document.getElementById('email').value;
//         const username = document.getElementById('username').value;

//         const ready =
//             email &&
//             username &&
//             consentCheckbox.checked &&
//             selectedPlatforms.length === 2;

//         startButton.disabled = !ready;
//         startButton.style.opacity = ready ? "1" : "0.5";
//     }

//     consentCheckbox.addEventListener('change', updateStartButton);
//     document.getElementById('username').addEventListener('input', updateStartButton);
//     document.getElementById('email').addEventListener('input', updateStartButton);

//     updateStartButton();
//     updateUI();

//     // 🚀 START ANALYSIS
//     startButton.addEventListener('click', async () => {

//         const email = localStorage.getItem("user_email");

//         if (!email) {
//             alert("Login first");
//             return;
//         }

//         try {
//             // 🔥 SEND EACH PLATFORM TO N8N
//             for (let platform of selectedPlatforms) {
//                 await fetch("https://phreatic-secundly-konner.ngrok-free.dev/webhook/predict-personality", {
//                     method: "POST",
//                     headers: {
//                         "Content-Type": "application/json"
//                     },
//                     body: JSON.stringify({
//                         user_id: email,
//                         platform: platform
//                     })
//                 });
//             }

//             alert("⏳ Analysis started...");

//             // 🔥 POLLING
//             const interval = setInterval(async () => {
//                 try {
//                     const res = await fetch(`http://127.0.0.1:8000/processed-data/${email}`);
//                     const data = await res.json();

//                     console.log("Polling:", data);

//                     if (data && data.metadata) {  // temp condition
//                         clearInterval(interval);

//                         alert("✅ Done!");

//                         chrome.tabs.create({
//                             url: "http://127.0.0.1:3000/dashboard.html?user_id=" + email
//                         });
//                     }

//                 } catch (err) {
//                     console.error(err);
//                 }
//             }, 3000);

//         } catch (err) {
//             console.error(err);
//             alert("Error starting analysis");
//         }

//     });

// });


document.addEventListener('DOMContentLoaded', () => {

    const loginButton = document.getElementById('login');
    const loginStatus = document.getElementById('loginStatus');
    const platforms = document.querySelectorAll('.platform');
    const consentCheckbox = document.getElementById('consent');
    const startButton = document.getElementById('start');
    const feedback = document.getElementById('platformSelectionFeedback');

    let selectedPlatforms = [];

    // 🔐 LOGIN
    loginButton.addEventListener('click', () => {
        const email = document.getElementById('email').value;

        if (!email) {
            loginStatus.textContent = "Enter email";
            loginStatus.style.color = "red";
            return;
        }

        localStorage.setItem("user_email", email);

        loginStatus.textContent = "✅ Logged in as " + email;
        loginStatus.style.color = "lightgreen";
    });

    // 🔥 PLATFORM SELECTION
    platforms.forEach(platform => {
        platform.addEventListener('click', () => {
            const value = platform.dataset.value;

            if (platform.classList.contains('active')) {
                platform.classList.remove('active');
                selectedPlatforms = selectedPlatforms.filter(p => p !== value);
            } else {
                if (selectedPlatforms.length >= 2) {
                    feedback.textContent = "Select only 2 platforms";
                    return;
                }
                platform.classList.add('active');
                selectedPlatforms.push(value);
            }

            updateUI();
        });
    });

    function updateUI() {
        if (selectedPlatforms.length === 1) {
            feedback.textContent = "Select one more platform";
        } else if (selectedPlatforms.length === 2) {
            feedback.textContent = "Ready ✅";
        } else {
            feedback.textContent = "Select 2 platforms";
        }

        updateStartButton();
    }

    function updateStartButton() {
        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;

        const ready =
            email &&
            username &&
            consentCheckbox.checked &&
            selectedPlatforms.length === 2;

        startButton.disabled = !ready;
    }

    consentCheckbox.addEventListener('change', updateStartButton);
    document.getElementById('username').addEventListener('input', updateStartButton);
    document.getElementById('email').addEventListener('input', updateStartButton);

    updateUI();

    // 🚀 START ANALYSIS
    startButton.addEventListener('click', async () => {

        const email = localStorage.getItem("user_email");

        try {
            // 🔥 SEND TO BACKEND
            for (let platform of selectedPlatforms) {
                await fetch("http://127.0.0.1:8000/receive-data", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        user_id: email,
                        platform: platform
                    })
                });
            }

            alert("⏳ Processing...");

            // 🔥 POLLING
            const interval = setInterval(async () => {
                const res = await fetch(`http://127.0.0.1:8000/processed-data/${user_id}`);
                const data = await res.json();

                if (data && data.ml_output) {
                    clearInterval(interval);

                    chrome.tabs.create({
                        url: "http://127.0.0.1:3000/dashboard.html?user_id=" + email
                    });
                }
            }, 3000);

        } catch (err) {
            console.error(err);
            alert("Error occurred");
        }

    });

});