
// const $cupcakeList =

// grab values from form
// make an post ajax request to /api/cupcakes endpoint with data
  //specify type, headers, send data in body
//turn response into object to work with
//update ui with new list
//use jquery to append on to the list

//function send get req to generate intial list
//func to handle UI (markup)
//function to make ajax request-
//controller function to handle json
//event listener for add button(prevent default)


const $FORM_DATA = $('.cupcakeForm');
const $CUPCAKE_LIST = $('.cupcakeList');
const $SUBMIT_BUTTON = $('#submitButton')

$SUBMIT_BUTTON.on('click',getFormDataAndCreateNewCupcake);


// function sayHi(e) {
//   e.preventDefault();
//   console.log("hello!");
// }


async function getFormDataAndCreateNewCupcake(event) {
  // createNewCupcake(
  //   handleFormSubmit()
  // );

  event.preventDefault();
  console.debug("made it here")
  const formData = getFormData();
  console.debug(formData);
  await createNewCupcake(formData);
  getCupcakeList()
}

/**
 * GET request for the list of cupcakes in the db
 */
async function getCupcakeList() {

  const response = await fetch ('/api/cupcakes');
  const cupcakesData = await response.json();

  console.log(cupcakesData)
  for(let cupcake in cupcakesData){
    let $cupcake = generateCupCakeMarkup(cupcake)
    $CUPCAKE_LIST.append($cupcake)
    }

}


/**
 * generate HTML
 */
function generateCupCakeMarkup(cupcake) {
return `
  <li>${cupcake.flavor}, ${cupcake.size}, ${cupcake.rating}</li>
`
}


function getFormData() {

  const flavor = $('#flavor').val();
  const size = $('#size').val();
  const rating = $('#rating').val();
  const imageUrl = $('#imageUrl').val();

  return {
    flavor,size,rating,imageUrl
  }

}


async function createNewCupcake(json) {
  console.log("accepts json:", json)

  // jsonify??
  const response = await fetch(
    `/api/cupcakes`,
    {
      method: "POST",
      body: JSON.stringify({json}),
      headers: {
        "Content-Type": "application/json"}
    }
  );
    const newCupcakeData = await response.json();

    const $newCupcake = generateCupCakeMarkup(newCupcakeData);
    $CUPCAKE_LIST.append($newCupcake);

}


