
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


$FORM_DATA = $('.cupcakeForm');
$CUPCAKE_LIST = $('.cupcakeList');

$FORM_DATA.on('submit',getFormDataAndDisplayList)



function getFormDataAndDisplayList() {
  createNewCupcake(
    handleFormSubmit()
  );


}

/**
 * GET request for the list of cupcakes in the db
 */
async function getCupcakeList() {

  const cupcakes = await fetch ('/api/cupcakes')

}


/**
 * lists cupcakes on homepage
 */
function generateCupCakeMarkup() {


}


function handleFormSubmit() {

  const flavor = $('#flavor').val();
  const size = $('#size').val();
  const rating = $('#rating').val();
  const imageUrl = $('#imageUrl').val();

  return jsonify(
    "flavor"=flavor,"size"=size,"rating"=rating,"imageUrl"=imageUrl
  )
}


async function createNewCupcake(json) {

  //fetch(api) {json}




}


