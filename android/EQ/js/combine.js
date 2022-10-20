// Credits: https://stackoverflow.com/a/51470002

function generateAllCombinationsOfText( array_of_arrays, wildcardReferences, text ){

    // First, handle some degenerate cases...

    if( ! array_of_arrays ){
        // Or maybe we should toss an exception...?
        return [];
    }

    if( ! Array.isArray( array_of_arrays ) ){
        // Or maybe we should toss an exception...?
        return [];
    }

    if( array_of_arrays.length == 0 ){
        return [];
    }

    for( let i = 0 ; i < array_of_arrays.length; i++ ){
        if( ! Array.isArray(array_of_arrays[i]) || array_of_arrays[i].length == 0 ){
            // If any of the arrays in array_of_arrays are not arrays or zero-length, return an empty array...
            return [];
        }
    }

    // Done with degenerate cases...

    // Start "odometer" with a 0 for each array in array_of_arrays.
    let odometer = new Array( array_of_arrays.length );
    odometer.fill( 0 ); 

    let output = [];

    let newCombination = formCombination( odometer, array_of_arrays, wildcardReferences, text );

    output.push( newCombination );

    while ( odometer_increment( odometer, array_of_arrays ) ){
        newCombination = formCombination( odometer, array_of_arrays, wildcardReferences, text );
        output.push( newCombination );
    }

    return output;
}/* combineArrays() */


// Translate "odometer" to combinations from array_of_arrays
function formCombination( odometer, array_of_arrays, wildcardReferences, text ){
    // In Imperative Programmingese (i.e., English):
    let tempText = text;
    for( let odometer_index=0; odometer_index < odometer.length; odometer_index++ ){
        let odometer_value = odometer[odometer_index];
        let wildcardToReplace = wildcardReferences[odometer_index];
        let wildcardValue = array_of_arrays[odometer_index][odometer_value];
        let regexReplace = new RegExp(escapeRegExp(wildcardToReplace), 'g');

        tempText = tempText.replace(regexReplace, wildcardValue);
    }
    return tempText;

    // In Functional Programmingese (Henny Youngman one-liner):
    // return odometer.reduce(
    //   function(accumulator, odometer_value, odometer_index){
    //     let wildcardToReplace = wildcardReferences[odometer_index];
    //     let wildcardValue = array_of_arrays[odometer_index][odometer_value];

    //     return "" + accumulator + array_of_arrays[odometer_index][odometer_value];
    //   },
    //   ""
    // );
}/* formCombination() */
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}
function odometer_increment( odometer, array_of_arrays ){

    // Basically, work you way from the rightmost digit of the "odometer"...
    // if you're able to increment without cycling that digit back to zero,
    // you're all done, otherwise, cycle that digit to zero and go one digit to the
    // left, and begin again until you're able to increment a digit
    // without cycling it...simple, huh...?

    for( let i_odometer_digit = odometer.length-1; i_odometer_digit >=0; i_odometer_digit-- ){ 

        let maxee = array_of_arrays[i_odometer_digit].length - 1;         

        if( odometer[i_odometer_digit] + 1 <= maxee ){
            // increment, and you're done...
            odometer[i_odometer_digit]++;
            return true;
        }
        else{
            if( i_odometer_digit - 1 < 0 ){
                // No more digits left to increment, end of the line...
                return false;
            }
            else{
                // Can't increment this digit, cycle it to zero and continue
                // the loop to go over to the next digit...
                odometer[i_odometer_digit]=0;
                continue;
            }
        }
    }/* for( let odometer_digit = odometer.length-1; odometer_digit >=0; odometer_digit-- ) */

}/* odometer_increment() */
