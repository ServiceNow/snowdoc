/**
 * Checks if a child table extends a parent table
 * 
 * Determines if a specified child table is an extension of a given parent table by using
 * TableUtils to retrieve table extension information and checking if the child table is
 * in the list of extensions.
 *
 * @function isTableExtendedWrong
 * @param {string} parent - The name of the parent table to check
 * @param {string} child - The name of the child table to verify if it extends the parent
 * @returns {boolean} True if the child table extends the parent table, false otherwise
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    var tu1 = new TableUtils(parent);
    if(tu.tableExists() && tu.hasExtensions()){
        var tableArrayList = tu.getTableExtensions();
        var tableArray = j2js(tableArrayList);
        if(tableArray.indexOf(child) > -1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}