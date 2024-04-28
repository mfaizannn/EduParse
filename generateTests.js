document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('pdfUpload');
    const amount = document.getElementById('amount');
    const test_type = document.getElementById('test_type');
    const generate = document.getElementById('generate');
    const result = document.getElementById('result');
    const apiUrl = "http://localhost:5000/upload";

    generate.addEventListener('click', () => {
        if (!fileInput.files[0]) {
            result.innerHTML = 'Please upload a PDF file.';
            return;
        }

        const formData = new FormData();
        formData.append('pdf', fileInput.files[0]);
        formData.append('numQuestions', amount.value);
        formData.append('type', test_type.value);

        fetch(apiUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                result.innerHTML = `Generated questions: ${data.questions}`;
            } else {
                result.innerHTML = `Error: ${data.message}`;
            }
        })
        .catch(error => {
            console.error('Request failed:', error);
            result.innerHTML = 'An error occurred, please try again later.';
        });
    });
});




// // document.addEventListener('DOMContentLoaded', function() {
// //     const fileInput = document.getElementById('pdfUpload');
// //     const amount = document.getElementById('amount');
// //     const test_type = document.getElementById('test_type');
// //     const generate = document.getElementById('generate');
// //     const result = document.getElementById('result');

// //     // set to the URL of the backend API that will process the PDF files and generate the tests.
// //     const apiUrl = "YOUR_API_URL_HERE"; // Set your API URL here
// //     const apiKey = "YOUR_API_KEY_HERE"; // Set your API key here

// //     generate.addEventListener('click', () => {
// //         if (!fileInput.files[0]) {
// //             result.innerHTML = 'Please upload a PDF file.';
// //             return;
// //         }

// //         const formData = new FormData();
// //         formData.append('file', fileInput.files[0]);
// //         formData.append('type', test_type.value);
// //         formData.append('amount', amount.value);

// //         fetch(apiUrl, {
// //             method: 'POST',
// //             headers: {
// //                 'X-API-KEY': apiKey
// //             },
// //             body: formData
// //         })
// //         // once api responds, this parses the json response
// //         .then(response => response.json())
// //         .then(data => {
// //             result.innerHTML = `Generated ${data.amount} questions of type ${data.type}`;
// //         })
// //         .catch(error => {
// //             console.error('Request failed:', error);
// //             result.innerHTML = 'An error occurred, please try again later.';
// //         });
// //     });
// // });


// document.addEventListener('DOMContentLoaded', function() {
//     const fileInput = document.getElementById('pdfUpload');
//     const amount = document.getElementById('amount');
//     const test_type = document.getElementById('test_type');
//     const generate = document.getElementById('generate');
//     const result = document.getElementById('result');

//     // Set to the URL of the backend API that will process the PDF files and generate the tests.
//     const apiUrl = "http://localhost:3000/upload"; // Set your API URL here

//     generate.addEventListener('click', () => {
//         if (!fileInput.files[0]) {
//             result.innerHTML = 'Please upload a PDF file.';
//             return;
//         }

//         const file = fileInput.files[0];
//         const reader = new FileReader();

//         reader.onload = function(event) {
//             const base64 = event.target.result.split(',')[1]; // Get base64 encoded PDF

//             fetch(apiUrl, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({
//                     pdf: base64,
//                     numQuestions: amount.value,
//                     type: test_type.value
//                 })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if(data.success) {
//                     result.innerHTML = `Generated questions: ${data.questions}`;
//                 } else {
//                     result.innerHTML = `Error: ${data.message}`;
//                 }
//             })
//             .catch(error => {
//                 console.error('Request failed:', error);
//                 result.innerHTML = 'An error occurred, please try again later.';
//             });
//         };

//         reader.readAsDataURL(file); // Read file as Data URL (base64)
//     });
// });
