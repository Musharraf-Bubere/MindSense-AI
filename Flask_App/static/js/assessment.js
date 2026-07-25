// ==========================================
// MindSense AI - Assessment Wizard
// ==========================================

const formSteps = document.querySelectorAll(".form-step");
const nextBtns = document.querySelectorAll(".next-btn");
const prevBtns = document.querySelectorAll(".prev-btn");

const progressBar = document.getElementById("progress-bar");

const steps = document.querySelectorAll(".step");

let currentStep = 0;


// ==========================================
// Show Current Step
// ==========================================

function showStep(step){

    formSteps.forEach((form)=>{

        form.classList.remove("active");

    });

    formSteps[step].classList.add("active");

    updateProgress();

}


// ==========================================
// Update Progress
// ==========================================

function updateProgress(){

    let percentage = ((currentStep + 1) / formSteps.length) * 100;

    progressBar.style.width = percentage + "%";

    progressBar.innerHTML = Math.round(percentage) + "%";


    steps.forEach((step,index)=>{

        step.classList.remove("active");
        step.classList.remove("completed");

        if(index < currentStep){

            step.classList.add("completed");

        }

        if(index === currentStep){

            step.classList.add("active");

        }

    });

}


// ==========================================
// Validate Current Step
// ==========================================

function validateStep(){

    const currentInputs = formSteps[currentStep].querySelectorAll(

        "input[required], select[required]"

    );

    let valid = true;

    currentInputs.forEach((input)=>{

        if(input.value.trim() === ""){

            input.classList.add("is-invalid");

            valid = false;

        }

        else{

            input.classList.remove("is-invalid");

        }

    });

    return valid;

}


// ==========================================
// Next Button
// ==========================================

nextBtns.forEach((button)=>{

    button.addEventListener("click",()=>{

        if(!validateStep()){

            alert("Please complete all required fields.");

            return;

        }

        if(currentStep < formSteps.length - 1){

            currentStep++;

            showStep(currentStep);

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        }

    });

});


// ==========================================
// Previous Button
// ==========================================

prevBtns.forEach((button)=>{

    button.addEventListener("click",()=>{

        if(currentStep > 0){

            currentStep--;

            showStep(currentStep);

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        }

    });

});


// ==========================================
// Live Validation
// ==========================================

const inputs = document.querySelectorAll(

    "input, select"

);

inputs.forEach((input)=>{

    input.addEventListener("change",()=>{

        if(input.value !== ""){

            input.classList.remove("is-invalid");

        }

    });

});


// ==========================================
// Initialize
// ==========================================

showStep(currentStep);