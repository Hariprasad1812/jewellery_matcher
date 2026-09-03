// ============================================================
// ELEMENTS
// ============================================================

const necklaceGrid =
    document.getElementById(
        "necklaceGrid"
    );

const imageInput =
    document.getElementById(
        "imageInput"
    );

const selectedSection =
    document.getElementById(
        "selectedSection"
    );

const selectedImage =
    document.getElementById(
        "selectedImage"
    );

const selectedName =
    document.getElementById(
        "selectedName"
    );

const matchButton =
    document.getElementById(
        "matchButton"
    );

const resetButton =
    document.getElementById(
        "resetButton"
    );

const loading =
    document.getElementById(
        "loading"
    );

const resultsSection =
    document.getElementById(
        "resultsSection"
    );

const resultsContainer =
    document.getElementById(
        "results"
    );


// ============================================================
// STATE
// ============================================================

let selectedSource = null;

let selectedFile = null;

let selectedOption = null;


// ============================================================
// PROVIDED NECKLACES
// ============================================================

const necklaces = [

    {
        id: "N01",
        name: "Necklace 01",
        file: "Nck_1.jpg"
    },

    {
        id: "N02",
        name: "Necklace 02",
        file: "Nck_2.jpg"
    },

    {
        id: "N03",
        name: "Necklace 03",
        file: "Nck_3.jpg"
    },

    {
        id: "N04",
        name: "Necklace 04",
        file: "Nck_4.jpg"
    },

    {
        id: "N05",
        name: "Necklace 05",
        file: "Nck_5.jpg"
    }

];


// ============================================================
// RENDER NECKLACES
// ============================================================

function renderNecklaces() {

    necklaceGrid.innerHTML = "";


    necklaces.forEach(
        (necklace, index) => {

            const option =
                document.createElement(
                    "div"
                );


            option.className =
                "necklace-option";


            option.dataset.file =
                necklace.file;


            option.innerHTML = `

                <img
                    src="/jewellery-image/${encodeURIComponent(necklace.file)}"
                    alt="${necklace.name}"
                >

                <div class="necklace-label">
                    ${necklace.name}
                </div>

                <div class="selected-check">
                    ✓
                </div>

            `;


            option.addEventListener(
                "click",
                () => {

                    selectProvidedNecklace(
                        necklace,
                        option
                    );

                }
            );


            necklaceGrid.appendChild(
                option
            );

        }
    );

}


// ============================================================
// SELECT PROVIDED NECKLACE
// ============================================================

async function selectProvidedNecklace(
    necklace,
    option
) {

    // Remove previous selection

    document
        .querySelectorAll(
            ".necklace-option"
        )
        .forEach(
            element => {
                element.classList.remove(
                    "selected"
                );
            }
        );


    option.classList.add(
        "selected"
    );


    selectedOption =
        option;


    selectedName.textContent =
        necklace.name;


    const imageURL =
        `/jewellery-image/${encodeURIComponent(
            necklace.file
        )}`;


    selectedImage.src =
        imageURL;


    selectedSection.classList.remove(
        "hidden"
    );


    resultsSection.classList.add(
        "hidden"
    );


    // Fetch supplied image and
    // convert it to a File object.

    try {

        const response =
            await fetch(
                imageURL
            );


        const blob =
            await response.blob();


        selectedFile =
            new File(
                [blob],
                necklace.file,
                {
                    type:
                        blob.type ||
                        "image/jpeg"
                }
            );


        selectedSource =
            "provided";

    } catch (error) {

        console.error(
            "Could not load necklace:",
            error
        );

        alert(
            "Could not load the selected necklace."
        );

    }

}


// ============================================================
// UPLOAD CUSTOM IMAGE
// ============================================================

imageInput.addEventListener(
    "change",
    function () {

        const file =
            this.files[0];


        if (!file) {
            return;
        }


        selectedFile =
            file;


        selectedSource =
            "upload";


        selectedName.textContent =
            file.name;


        const previewURL =
            URL.createObjectURL(
                file
            );


        selectedImage.src =
            previewURL;


        // Remove provided selection

        document
            .querySelectorAll(
                ".necklace-option"
            )
            .forEach(
                element => {
                    element.classList.remove(
                        "selected"
                    );
                }
            );


        selectedSection.classList.remove(
            "hidden"
        );


        resultsSection.classList.add(
            "hidden"
        );

    }
);


// ============================================================
// MATCH BUTTON
// ============================================================

matchButton.addEventListener(
    "click",
    async function () {

        if (!selectedFile) {

            alert(
                "Please select a necklace first."
            );

            return;
        }


        // Show loading

        loading.classList.remove(
            "hidden"
        );


        resultsSection.classList.add(
            "hidden"
        );


        matchButton.disabled =
            true;


        resetButton.disabled =
            true;


        // Create multipart form

        const formData =
            new FormData();


        formData.append(
            "file",
            selectedFile
        );


        try {

            const response =
                await fetch(
                    "/match",
                    {
                        method:
                            "POST",

                        body:
                            formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Matching failed."
                );

            }


            displayResults(
                data.matches
            );


        } catch (error) {

            console.error(
                error
            );


            alert(
                "Something went wrong: " +
                error.message
            );


        } finally {

            loading.classList.add(
                "hidden"
            );


            matchButton.disabled =
                false;


            resetButton.disabled =
                false;

        }

    }
);


// ============================================================
// DISPLAY RESULTS
// ============================================================

function displayResults(
    matches
) {

    resultsContainer.innerHTML =
        "";


    if (
        !matches ||
        matches.length === 0
    ) {

        resultsContainer.innerHTML = `

            <div class="empty-state">
                No matching earrings found.
            </div>

        `;

        resultsSection.classList.remove(
            "hidden"
        );

        return;
    }


    matches.forEach(
        (item, index) => {

            const similarity =
                Number(
                    item.similarity
                );


            // Keep score as the
            // actual similarity value.
            // We display it on a 0-100 scale
            // only as a visual similarity score.

            const score =
                (
                    similarity * 100
                ).toFixed(1);


            const card =
                document.createElement(
                    "article"
                );


            card.className =
                "result-card";


            card.innerHTML = `

                <div class="rank">
                    #${index + 1}
                </div>

                <img
                    src="/jewellery-image/${encodeURIComponent(
                        item.image_file
                    )}"
                    alt="Matching earring ${item.id}"
                >

                <div class="result-info">

                    <div class="result-title">

                        <h3>
                            Match #${index + 1}
                        </h3>

                        <span class="product-id">
                            ${item.id}
                        </span>

                    </div>

                    <div class="score-row">

                        <span class="score-label">
                            Visual similarity
                        </span>

                        <span class="score-value">
                            ${score}%
                        </span>

                    </div>

                </div>

            `;


            resultsContainer.appendChild(
                card
            );

        }
    );


    resultsSection.classList.remove(
        "hidden"
    );


    // Scroll to results

    setTimeout(
        () => {

            resultsSection.scrollIntoView(
                {
                    behavior:
                        "smooth",
                    block:
                        "start"
                }
            );

        },
        100
    );

}


// ============================================================
// RESET
// ============================================================

resetButton.addEventListener(
    "click",
    function () {

        selectedFile =
            null;

        selectedSource =
            null;

        selectedOption =
            null;


        imageInput.value =
            "";


        selectedSection.classList.add(
            "hidden"
        );


        resultsSection.classList.add(
            "hidden"
        );


        resultsContainer.innerHTML =
            "";


        document
            .querySelectorAll(
                ".necklace-option"
            )
            .forEach(
                element => {

                    element.classList.remove(
                        "selected"
                    );

                }
            );


        window.scrollTo(
            {
                top: 0,
                behavior: "smooth"
            }
        );

    }
);


// ============================================================
// INITIALIZE
// ============================================================

renderNecklaces();